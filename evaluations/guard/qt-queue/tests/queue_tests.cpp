#include "frame_queue.h"
#include <iostream>
#include <string>

int main(int argc, char** argv) {
    if (argc != 2) { return 2; }
    const std::string name(argv[1]);
    FrameQueue queue(4);
    int value = -1;
    bool passed = false;
    if (name == "empty") {
        passed = !queue.pop(value) && value == -1;
    } else if (name == "zero") {
        bool zero_rejected = false;
        bool negative_rejected = false;
        try { FrameQueue invalid(0); } catch (const std::invalid_argument&) { zero_rejected = true; }
        try { FrameQueue invalid(-1); } catch (const std::invalid_argument&) { negative_rejected = true; }
        passed = zero_rejected && negative_rejected;
    } else if (name == "fifo") {
        queue.push(10);
        queue.push(20);
        passed = queue.pop(value) && value == 10 && queue.pop(value) && value == 20 && !queue.pop(value);
    } else if (name == "capacity") {
        FrameQueue single(1);
        single.push(10);
        single.push(20);
        passed = single.size() == 1 && single.pop(value) && value == 20;
    } else if (name == "overload") {
        passed = true;
        for (int i = 0; i < 10000; ++i) {
            queue.push(i);
            if (queue.size() > 4) { passed = false; }
        }
        std::cout << "produced=10000 consumed=0 retained=" << queue.size() << " capacity=4\n";
        for (int expected = 9996; expected < 10000; ++expected) {
            if (!queue.pop(value) || value != expected) { passed = false; }
        }
        if (queue.pop(value)) { passed = false; }
    } else {
        return 2;
    }
    std::cout << (passed ? "PASS " : "FAIL ") << name << '\n';
    return passed ? 0 : 1;
}
