# Qt 队列风险发现示例

这是可编译运行的 QtCore / C++14 小项目。使用整数编号演示容量约束：最多保留 4 条，满载时丢弃最旧编号。代码限定同一线程使用。它不包含视频、QML、WebRTC、Android 或网络，不测延迟、内存峰值与线程竞争。

## 文件与运行

- `src/frame_queue.h`：有界实现。
- `negative-control/frame_queue.h`：故意保留无界缺陷的对照输入，不用于业务集成。
- `tests/queue_tests.cpp`：两个实现共用的行为测试。
- `CMakeLists.txt`：构建两个测试程序，CTest 只收录正确实现的 5 项测试。
- [工程记录](engineering-notes.md)：事实、验收、设计、测试、审查和交付范围。
- [.engineering/run.yaml](.engineering/run.yaml)：本示例当前证据记录。

本次验证环境为 Windows、Visual Studio 2019、MSVC 19.29.30159.0、Win32、Windows SDK 10.0.19041.0、CMake 3.25.1、Qt 5.15.6。使用本机已有 SDK，未下载或打包 Qt。

在本目录执行，按实际安装位置设置 Qt 前缀并使对应 `bin` 目录处于 PATH：

```powershell
$qtPrefix = 'C:/Qt/qt-5.15.6-compiled-msvc2017-x86/qt-5.15.6-compiled-msvc2017-x86'
$env:PATH = "$qtPrefix/bin;$env:PATH"
cmake -S . -B build -G 'Visual Studio 16 2019' -A Win32 "-DCMAKE_PREFIX_PATH=$qtPrefix"
cmake --build build --config Release --parallel 2
ctest --test-dir build -C Release --output-on-failure
./build/Release/queue_negative_control.exe overload
# 预期 exit 1，retained=10000，FAIL overload。
./build/Release/queue_tests.exe overload
# 预期 exit 0，retained=4，PASS overload。
```

从 Project Engineering 根目录复核本次已保存证据：

```powershell
python -m pip install -r requirements.txt
python scripts/engineering_guard.py check --project evaluations/guard/qt-queue --stage delivery
```

该命令只检查记录。重新构建/测试后应保存新的输出、审查差异并更新记录与 SHA-256；不可把旧记录当作本次运行结果。

本次交付为示例源码、说明与日志，`build/` 不纳入版本控制。没有打包运行库、安装程序或发布产物；其他平台、SDK 来源与分发许可条件需要在真实发布任务中重新核对。
