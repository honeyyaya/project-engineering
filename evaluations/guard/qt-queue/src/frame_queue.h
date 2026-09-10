#pragma once

#include <QQueue>
#include <stdexcept>

// Thread-confined integer frame IDs. Payload ownership and real video are out of scope.
class FrameQueue {
public:
    explicit FrameQueue(int capacity) : capacity_(capacity) {
        if (capacity <= 0) {
            throw std::invalid_argument("capacity must be positive");
        }
    }

    void push(int frame) {
        if (frames_.size() == capacity_) {
            frames_.dequeue();
        }
        frames_.enqueue(frame);
    }

    bool pop(int& frame) {
        if (frames_.isEmpty()) {
            return false;
        }
        frame = frames_.dequeue();
        return true;
    }

    int size() const { return frames_.size(); }

private:
    int capacity_;
    QQueue<int> frames_;
};
