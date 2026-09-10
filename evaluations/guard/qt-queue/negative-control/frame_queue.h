#pragma once

#include <QQueue>
#include <stdexcept>

// Intentionally unbounded test baseline. Not an application implementation.
class FrameQueue {
public:
    explicit FrameQueue(int capacity) {
        if (capacity <= 0) {
            throw std::invalid_argument("capacity must be positive");
        }
    }
    void push(int frame) { frames_.enqueue(frame); }
    bool pop(int& frame) {
        if (frames_.isEmpty()) {
            return false;
        }
        frame = frames_.dequeue();
        return true;
    }
    int size() const { return frames_.size(); }
private:
    QQueue<int> frames_;
};
