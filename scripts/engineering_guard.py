"""Check recorded engineering evidence; this is not a static analyzer or scheduler."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
RECORD = Path('.engineering/run.yaml')


def read_yaml(path):
    value = yaml.safe_load(path.read_text(encoding='utf-8-sig'))
    if not isinstance(value, dict):
        raise ValueError(f'{path}: expected a mapping')
    return value


def indexed(items, label):
    if not isinstance(items, list):
        raise ValueError(f'{label}: expected a list')
    result = {}
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get('id'), str) or not item['id'].strip():
            raise ValueError(f'{label}: expected a mapping with a nonempty id')
        key = item['id']
        if key in result:
            raise ValueError(f'duplicate {label}: {key}')
        result[key] = item
    return result


def feature_tags(value):
    allowed = read_yaml(ROOT / 'registry/risks.yaml')['features']
    if not isinstance(value, list) or any(not isinstance(tag, str) for tag in value):
        raise ValueError('features must be a list of registered names')
    if not set(value) <= set(allowed):
        raise ValueError(f'unknown features: {sorted(set(value) - set(allowed))}')
    return set(value)


def has_reason(value):
    return isinstance(value, str) and bool(value.strip())


def configuration():
    roles = indexed(read_yaml(ROOT / 'registry/roles.yaml')['roles'], 'role')
    risks = indexed(read_yaml(ROOT / 'registry/risks.yaml')['risks'], 'risk')
    gates = indexed(read_yaml(ROOT / 'registry/gates.yaml')['gates'], 'gate')
    skills = indexed(read_yaml(ROOT / 'registry/skills.yaml')['skills'], 'skill')
    stack = read_yaml(ROOT / 'stack/project-engineering.yaml')
    for role in roles.values():
        if not (ROOT / role['path']).is_file():
            raise ValueError(f'missing role file: {role["path"]}')
    for risk in risks.values():
        feature_tags(risk['any_features'])
        if risk['category'] not in read_yaml(ROOT / 'registry/risks.yaml')['categories']:
            raise ValueError(f'unknown risk category: {risk["id"]}')
        if risk['owner'] not in roles or not set(risk['stages']) <= gates.keys():
            raise ValueError(f'invalid owner or stages: {risk["id"]}')
        for skill in risk['components']:
            if skill not in skills:
                raise ValueError(f'unknown component: {skill}')
    for gate in gates.values():
        if not (ROOT / gate['policy']).is_file():
            raise ValueError(f'missing gate policy: {gate["policy"]}')
    for flow in stack['default_workflows'].values():
        if not set(flow['stages']) <= gates.keys():
            raise ValueError('workflow references an unknown gate')
    for path in stack['profiles'].values():
        profile = read_yaml(ROOT / path)
        feature_tags(profile['guard']['base_features'])
        for group in ('skills', 'superpowers'):
            for items in profile[group].values():
                if not set(items) <= skills.keys():
                    raise ValueError(f'unknown profile components in {path}')
    return roles, risks, gates, skills, stack


def init_project(project, profile_name, workflow, features):
    _, _, _, _, stack = configuration()
    profiles = {read_yaml(ROOT / path)['profile']: path for path in stack['profiles'].values()}
    if profile_name not in profiles or workflow not in stack['default_workflows']:
        raise ValueError('unknown profile or workflow')
    record = project / RECORD
    if record.exists():
        raise ValueError(f'refusing to overwrite {record}')
    profile = read_yaml(ROOT / profiles[profile_name])
    tags = sorted(feature_tags(profile['guard']['base_features'] + features))
    data = {
        'schema_version': '0.1',
        'project': {'name': project.name, 'profile': profile_name, 'revision': 'initial'},
        'workflow': workflow,
        'current_stage': stack['default_workflows'][workflow]['stages'][0],
        'features': tags,
        'selected_components': [],
        'artifacts': [],
        'checks': [],
        'issues': [],
    }
    record.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation also prevents overwrites when two initializations race.
    with record.open('x', encoding='utf-8') as stream:
        yaml.safe_dump(data, stream, allow_unicode=True, sort_keys=False)
    return record


def evidence_errors(project, evidence):
    if not isinstance(evidence, list) or not evidence:
        return ['missing evidence']
    errors = []
    for item in evidence:
        if not isinstance(item, dict) or not isinstance(item.get('path'), str) or not item['path'].strip():
            raise ValueError('evidence requires a nonempty path')
        path = (project / item['path']).resolve()
        if not path.is_relative_to(project.resolve()):
            errors.append('evidence must be inside the target project')
        elif not path.is_file() or path.stat().st_size == 0:
            errors.append(f'missing/empty evidence: {item["path"]}')
        elif hashlib.sha256(path.read_bytes()).hexdigest() != item.get('sha256'):
            errors.append(f'changed evidence: {item["path"]}')
    return errors


def evaluate(project, data, stage=None):
    roles, risks, gates, skills, stack = configuration()
    if data.get('schema_version') != '0.1':
        raise ValueError('unsupported run schema')
    profiles = {read_yaml(ROOT / p)['profile']: read_yaml(ROOT / p) for p in stack['profiles'].values()}
    profile = profiles[data['project']['profile']]
    stages = stack['default_workflows'][data['workflow']]['stages']
    stage = stage or data['current_stage']
    if stage not in stages or data['current_stage'] not in stages:
        raise ValueError('stage is not in the selected workflow')
    revision = data['project']['revision']
    if not isinstance(revision, str) or not revision.strip():
        raise ValueError('project revision is required')
    features = feature_tags(data['features'])
    if not set(profile['guard']['base_features']) <= features:
        raise ValueError('profile base features cannot be removed')
    selected = indexed(data['selected_components'], 'selected component')
    for key, selection in selected.items():
        if key not in skills or selection['mode'] not in ('reference', 'evaluation', 'default'):
            raise ValueError(f'invalid component selection: {key}')
        if selection['mode'] == 'default' and skills[key]['maturity'] != 'S4':
            raise ValueError(f'component is not S4 Core: {key}')
    artifacts = indexed(data['artifacts'], 'artifact')
    checks = {}
    for check in data['checks']:
        key = (check['stage'], check['risk_id'])
        if key in checks or key[0] not in stages or key[1] not in risks:
            raise ValueError(f'duplicate or unknown check: {key}')
        if check['discovered_by'] not in roles:
            raise ValueError(f'unknown check role: {check["discovered_by"]}')
        if not set(check['components']) <= selected.keys():
            raise ValueError('check uses an unrecorded component')
        checks[key] = check
    issues = indexed(data['issues'], 'issue')
    results = []
    for phase in stages[:stages.index(stage) + 1]:
        reasons = []
        for name in gates[phase]['artifacts']:
            artifact = artifacts.get(name)
            if artifact is None or artifact.get('revision') != revision:
                reasons.append(f'{name}: missing or stale artifact')
            else:
                reasons += [f'{name}: {e}' for e in evidence_errors(project, artifact.get('evidence'))]
        required = [r for r in risks.values() if phase in r['stages'] and
                    (not r['any_features'] or set(r['any_features']) & features)]
        for risk in required:
            check = checks.get((phase, risk['id']))
            prefix = risk['id']
            if check is None:
                reasons.append(f'{prefix}: unverified; owner={risk["owner"]}')
                continue
            if check.get('revision') != revision:
                reasons.append(f'{prefix}: stale check')
            if check.get('status') not in ('passed', 'not-applicable'):
                reasons.append(f'{prefix}: {check.get("status", "unverified")}')
            if not has_reason(check.get('reason')):
                reasons.append(f'{prefix}: decision reason required')
            reasons += [f'{prefix}: {e}' for e in evidence_errors(project, check.get('evidence'))]
        results.append({'stage': phase, 'status': 'blocked' if reasons else 'passed', 'reasons': reasons})
    issue_errors = []
    for issue in issues.values():
        if issue['risk_id'] not in risks or issue['owner'] not in roles:
            raise ValueError(f'unknown issue risk or owner: {issue["id"]}')
        if issue['severity'] not in ('blocker', 'high', 'medium', 'low'):
            raise ValueError(f'invalid issue severity: {issue["id"]}')
        status = issue['status']
        if status not in ('open', 'mitigated', 'verified', 'accepted', 'dismissed'):
            raise ValueError(f'invalid issue status: {issue["id"]}')
        if status in ('verified', 'dismissed', 'accepted'):
            issue_errors += [f'{issue["id"]}: {e}' for e in evidence_errors(project, issue.get('evidence'))]
            if issue.get('revision') != revision or not has_reason(issue.get('reason')):
                issue_errors.append(f'{issue["id"]}: stale or unexplained disposition')
        if status == 'accepted' and (not issue.get('accepted_by') or issue['severity'] in ('blocker', 'high')):
            issue_errors.append(f'{issue["id"]}: acceptance cannot clear this issue')
        if status in ('open', 'mitigated') and (issue['severity'] in ('blocker', 'high') or stage == 'delivery'):
            issue_errors.append(f'{issue["id"]}: unresolved {issue["severity"]} issue')
    return {'stage': stage, 'status': 'blocked' if issue_errors or any(r['status'] == 'blocked' for r in results) else 'passed',
            'gates': results, 'issue_errors': issue_errors,
            'scope': 'Recorded evidence only; semantic review and tool execution remain with the agent/reviewer.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('validate', help='validate the guard catalog and component references')
    init = commands.add_parser('init', help='create a project-local evidence record, not application code')
    init.add_argument('--project', type=Path, required=True)
    init.add_argument('--profile', default='qt-project')
    init.add_argument('--workflow', default='new_project')
    init.add_argument('--features', nargs='*', default=[])
    check = commands.add_parser('check', help='check this gate and every preceding gate')
    check.add_argument('--project', type=Path, required=True)
    check.add_argument('--stage')
    args = parser.parse_args()
    try:
        if args.command == 'validate':
            roles, risks, gates, skills, _ = configuration()
            print(json.dumps({'roles': len(roles), 'risks': len(risks), 'gates': len(gates), 'skills': len(skills)}))
            return 0
        if args.command == 'init':
            print(init_project(args.project.resolve(), args.profile, args.workflow, args.features))
            return 0
        result = evaluate(args.project.resolve(), read_yaml(args.project / RECORD), args.stage)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result['status'] == 'passed' else 1
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as error:
        print(f'Invalid guard input: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
