#pragma once
#include <bitset>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#ifndef INTERPRET_H
#define INTERPRET_H

class Interpret {
public:
    Interpret(const std::string &binaryFile, const std::string &resultFile, size_t start, size_t end,
              bool debug = false);

private:
    std::vector<uint32_t> memory = std::vector<uint32_t>(1024, 0);
    std::vector<uint32_t> registers = std::vector<uint32_t>(32, 0);
    bool debug;

private:
    void debugOutput() const;
    template<int N>
    std::bitset<N> readBitsetFromBinaryFile(std::istream &is);
    void loadConstantFromCode(std::bitset<48> code);
    void memoryReadFromCode(std::bitset<48> code);
    void memoryWriteFromCode(std::bitset<48> code);
    void bitwiseOrFromCode(std::bitset<48> code);
    void saveMemoryToYAML(const std::string &resultFile, size_t start, size_t end) const;
};

#endif // INTERPRET_H
