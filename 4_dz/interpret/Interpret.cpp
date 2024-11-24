#include "Interpret.h"

void Interpret::debugOutput() const {
    // Вывод регистров
    std::cout << "Registers: ";
    for (size_t i = 0; i < registers.size(); ++i) {
        std::cout << "R" << i << ":" << registers[i] << " ";
    }
    std::cout << "\nMemory: ";
    // Вывод первых 16 ячеек памяти
    for (size_t i = 0; i < 16; ++i) {
        std::cout << "M" << i << ":" << memory[i] << " ";
    }
    std::cout << "\n\n";
}

template<int N>
std::bitset<N> Interpret::readBitsetFromBinaryFile(std::istream &is) {
    std::bitset<N> code;
    for (int i = 0; i < N / 8; i++) {
        unsigned char byte;
        if (is.read(reinterpret_cast<char *>(&byte), sizeof(byte))) {
            code |= std::bitset<N>(byte) << (i * 8);
        }
    }
    return code;
}

// Функция для декодирования loadConstant из считанного битсета
void Interpret::loadConstantFromCode(const std::bitset<48> code) {
    const unsigned int A = (code.to_ulong() >> 0) & 0xFF; // 8 бит
    const unsigned int B = (code.to_ulong() >> 8) & 0x7; // 3 бита
    const unsigned int C = (code.to_ulong() >> 11) & 0xFFFFFF; // 24 бита

    if (A != 195) {
        std::cerr << "Invalid opcode for LOAD_CONSTANT: " << A << "\n";
        return;
    }

    if (debug) {
        std::cout << "LOAD_CONSTANT: A=" << A << ", B=" << B << ", C=" << C << "\n";
    }
    registers[B] = C;
}

// Функция для декодирования memoryRead из считанного битсета
void Interpret::memoryReadFromCode(const std::bitset<48> code) {
    const unsigned int A = (code.to_ulong() >> 0) & 0xFF; // 8 бит
    const unsigned int B = (code.to_ulong() >> 8) & 0x7; // 3 бита
    const unsigned int C = (code.to_ulong() >> 11) & 0x7; // 3 бита

    if (A != 83) {
        std::cerr << "Invalid opcode for MEMORY_READ: " << A << "\n";
        return;
    }

    if (B >= registers.size() || C >= memory.size()) {
        std::cerr << "Out-of-bounds access in MEMORY_READ: B=" << B << ", C=" << C << "\n";
        return;
    }

    registers[C] = memory[registers[B]];
    if (debug) {
        std::cout << "MEMORY_READ: A=" << A << ", B=" << B << ", C=" << C << "\n";
    }
}

// Функция для декодирования memoryWrite из считанного битсета
void Interpret::memoryWriteFromCode(const std::bitset<48> code) {
    const unsigned int A = (code.to_ulong() >> 0) & 0xFF; // 8 бит
    const unsigned int B = (code.to_ulong() >> 8) & 0x7; // 3 бита
    const unsigned int C = (code.to_ulong() >> 11) & 0x1FF; // 9 бит
    const unsigned int D = (code.to_ulong() >> 20) & 0x7; // 3 бита

    if (A != 53) {
        std::cerr << "Invalid opcode for MEMORY_WRITE: " << A << "\n";
        return;
    }

    if (B >= registers.size() || D >= registers.size() || registers[D] + C >= memory.size()) {
        std::cerr << "Out-of-bounds access in MEMORY_WRITE: B=" << B << ", C=" << C << ", D=" << D << "\n";
        return;
    }

    memory[registers[D] + C] = registers[B];
    if (debug) {
        std::cout << "MEMORY_WRITE: A=" << A << ", B=" << B << ", C=" << C << ", D=" << D << "\n";
    }
}

// Функция для декодирования bitwiseOr из считанного битсета
void Interpret::bitwiseOrFromCode(const std::bitset<48> code) {
    const unsigned int A = (code.to_ulong() >> 0) & 0xFF; // 8 бит
    const unsigned int B = (code.to_ulong() >> 8) & 0x7; // 3 бита
    const unsigned int C = (code.to_ulong() >> 11) & 0x1FFFFF; // 21 бит
    const unsigned int D = (code.to_ulong() >> 38) & 0x7; // 3 бита

    if (A != 74) {
        std::cerr << "Invalid opcode for BITWISE_OR: " << A << "\n";
        return;
    }
    if (B >= registers.size() || D >= registers.size() || C >= memory.size()) {
        std::cerr << "Out-of-bounds access in BITWISE_OR: B=" << B << ", C=" << C << ", D=" << D << "\n";
        return;
    }
    std::cout << B << " " << C << " " << D << std::endl;
    registers[B] = registers[D] | memory[C];
    if (debug) {
        std::cout << "BITWISE_OR: A=" << A << ", B=" << B << ", C=" << C << ", D=" << D << "\n";
    }
}

// Изменим функцию executeBinaryFile для проверки типа команды и чтения
// соответствующего количества байт
Interpret::Interpret(const std::string &binaryFile, const std::string &resultFile, const size_t start, const size_t end,
                     const bool debug) {
    this->debug = debug;
    std::ifstream infile(binaryFile, std::ios::binary);
    if (!infile) {
        std::cerr << "Error opening binary file." << std::endl;
        return;
    }


    while (infile.peek() != EOF) {
        auto code = readBitsetFromBinaryFile<48>(infile);

        // Декодирование команды
        unsigned int A = (code >> 0).to_ulong() & 0xFF;
        if (A == 195) {
            loadConstantFromCode(code);
        } else if (A == 83) {
            memoryReadFromCode(code);
        } else if (A == 53) {
            memoryWriteFromCode(code);
        } else if (A == 74) {
            bitwiseOrFromCode(code);
        } else {
            std::cerr << "Unknown command A=" << A << "\n";
        }

        if (debug) {
            debugOutput();
        }
    }
    saveMemoryToYAML(resultFile, start, end);
}

void Interpret::saveMemoryToYAML(const std::string &resultFile, size_t start, size_t end) const {
    std::ofstream out(resultFile);
    out << "memory:" << std::endl;

    for (size_t i = start; i <= end && i < memory.size(); ++i) {
        out << "  - ID: " << i << std::endl;
        out << "    VALUE: " << memory[i] << std::endl;
    }
}
