#include "Assemble.h"

template<int N>
void Assemble::writeBitsetToBinaryFile(const std::bitset<N> &code) {

    for (int i = 0; i < N / 8; i++) {
        unsigned char byte = (code >> (i * 8)).to_ulong() & 0xFF;
        os.write(reinterpret_cast<const char *>(&byte), sizeof(byte));
    }
}

void Assemble::loadConstant(const unsigned int B, const unsigned int C) {
    std::bitset<48> code;
    constexpr unsigned int A = 195;

    for (int i = 0; i <= 7; i++)
        code[i] = (A >> i) & 1;
    for (int i = 8; i <= 10; i++)
        code[i] = (B >> (i - 8)) & 1;
    for (int i = 11; i <= 36; i++)
        code[i] = (C >> (i - 11)) & 1;

    writeBitsetToBinaryFile<48>(code);
}

void Assemble::memoryRead(const unsigned int B, const unsigned int C) {
    std::bitset<48> code;
    constexpr unsigned int A = 83;

    for (int i = 0; i <= 7; i++)
        code[i] = (A >> i) & 1;
    for (int i = 8; i <= 10; i++)
        code[i] = (B >> (i - 8)) & 1;
    for (int i = 11; i <= 13; i++)
        code[i] = (C >> (i - 11)) & 1;

    writeBitsetToBinaryFile<48>(code);
}

void Assemble::memoryWrite(const unsigned int B, const unsigned int C, const unsigned int D) {
    std::bitset<48> code;
    constexpr unsigned int A = 53;

    for (int i = 0; i <= 7; i++)
        code[i] = (A >> i) & 1;
    for (int i = 8; i <= 10; i++)
        code[i] = (B >> (i - 8)) & 1;
    for (int i = 11; i <= 19; i++)
        code[i] = (C >> (i - 11)) & 1;
    for (int i = 20; i <= 22; i++)
        code[i] = (D >> (i - 20)) & 1;

    writeBitsetToBinaryFile<48>(code);
}

void Assemble::bitwiseOr(const unsigned int B, const unsigned int C, const unsigned int D) {
    std::bitset<48> code;
    constexpr unsigned int A = 74;

    for (int i = 0; i <= 7; i++)
        code[i] = (A >> i) & 1;
    for (int i = 8; i <= 10; i++)
        code[i] = (B >> (i - 8)) & 1;
    for (int i = 11; i <= 37; i++)
        code[i] = (C >> (i - 11)) & 1;
    for (int i = 38; i <= 40; i++)
        code[i] = (D >> (i - 38)) & 1;

    writeBitsetToBinaryFile<48>(code);
}

Assemble::Assemble(const std::string &inputFile, const std::string &outputFile, const std::string &logFile) {
    std::ifstream infile(inputFile);
    os = std::ofstream(outputFile, std::ios::binary);
    std::ofstream logfile(logFile);
    if (!infile || !os || !logfile) {
        logfile << "Error opening files." << std::endl;
        return;
    }

    std::string input, reg, operand;
    std::string plus, shift;
    unsigned int regAddr, value, addr, offset;

    while (infile >> input) {
        if (input == "LOAD_CONSTANT") {
            try {
                infile >> reg >> operand;
                if (reg[reg.size() - 1] != ',') {
                    throw std::invalid_argument("Missing comma");
                }
                if (reg.empty() || reg[0] != 'R') {
                    throw std::invalid_argument("Invalid register");
                }
                if (operand.empty() || operand[0] != '#') {
                    throw std::invalid_argument("Invalid operand");
                }
                regAddr = std::stoi(reg.substr(1, reg.size() - 1));
                value = std::stoi(operand.substr(1));

                loadConstant(regAddr, value);
                // TODO Исправлен порядок, в интерпретаторе учесть
                logfile << "- type: LOAD_CONSTANT" << std::endl;
                logfile << "  A: " << 195 << std::endl;
                logfile << "  B: " << std::endl;
                logfile << "    value: " << regAddr << std::endl;
                logfile << "  C: " << std::endl;
                logfile << "    value: " << value << std::endl;

            } catch (std::invalid_argument &e) {
                std::cerr << "Syntax error. Load constant failed. " << inputFile << "\n" << e.what() << std::endl;
                std::cerr << "input: '" << input << "', register: '" << reg << "', operand: '" << operand << "'"
                          << std::endl;
                return;
            } catch (...) {
                std::cerr << "Syntax error. Load constant failed. " << inputFile << std::endl;
                std::cerr << "input: '" << input << "', register: '" << reg << "', operand: '" << operand << "'"
                          << std::endl;
                return;
            }
        } else if (input == "MEMORY_READ") {
            try {
                infile >> reg >> operand;
                if (reg[reg.size() - 1] != ',') {
                    throw std::invalid_argument("Missing comma");
                }
                if (reg.empty() || reg[0] != 'R') {
                    throw std::invalid_argument("Invalid register");
                }
                if (operand.empty() || operand[0] != '[' || operand[operand.size() - 1] != ']') {
                    throw std::invalid_argument("Invalid operand");
                }
                regAddr = std::stoi(reg.substr(1, reg.size() - 1));
                addr = std::stoi(operand.substr(2, operand.size() - 3));
                std::stoi(reg.substr(1, reg.size() - 1));

                memoryRead(addr, regAddr);
                // TODO Исправлен порядок, в интерпретаторе уч
                logfile << "- type: MEMORY_READ" << std::endl;
                logfile << "  A: " << 83 << std::endl;
                logfile << "  B: " << std::endl;
                logfile << "    value: " << addr << std::endl;
                logfile << "  C: " << std::endl;
                logfile << "    value: " << regAddr << std::endl;
            } catch (std::invalid_argument &e) {
                std::cerr << "Syntax error. Memory read failed. " << inputFile << "\n" << e.what() << std::endl;
                std::cerr << "input: '" << input << "', register: '" << reg << "', operand: '" << operand << "'"
                          << std::endl;
                return;
            } catch (...) {
                std::cerr << "Syntax error. Memory read failed " << inputFile << std::endl;
                std::cerr << "input: '" << input << "', register: '" << reg << "', operand: '" << operand << "'"
                          << std::endl;
                return;
            }

        } else if (input == "MEMORY_WRITE") {
            try {
                infile >> operand >> plus >> shift >> reg;
                if (shift[shift.size() - 1] != ',') {
                    throw std::invalid_argument("Missing comma");
                }
                if (plus != "+") {
                    throw std::invalid_argument("Missing plus");
                }
                if (reg.empty() || reg[0] != 'R') {
                    throw std::invalid_argument("Invalid register");
                }
                if (operand[0] != '[' || shift[shift.size() - 2] != ']' || operand[1] != 'R') {
                    throw std::invalid_argument("Invalid operand");
                }

                regAddr = std::stoi(operand.substr(2));
                offset = std::stoi(shift.substr(0, shift.size() - 2));
                value = std::stoi(reg.substr(1));

                memoryWrite(value, offset, regAddr);
                // TODO Исправлен порядок, в интерпретаторе уч
                logfile << "- type: MEMORY_WRITE" << std::endl;
                logfile << "  A: " << 53 << std::endl;
                logfile << "  B: " << std::endl;
                logfile << "    value: " << value << std::endl;
                logfile << "  C: " << std::endl;
                logfile << "    value: " << offset << std::endl;
                logfile << "  D: " << std::endl;
                logfile << "    value: " << regAddr << std::endl;
            } catch (std::invalid_argument &e) {
                std::cerr << "Syntax error. Memory write failed. " << inputFile << "\n" << e.what() << std::endl;
                std::cerr << "input: '" << input << "', operand: '" << operand << " " << plus << " " << shift
                          << "', reg: '" << reg << "'" << std::endl;
                return;
            } catch (...) {
                std::cerr << "Syntax error. Memory write failed. " << inputFile << std::endl;
                std::cerr << "input: '" << input << "', operand: '" << operand << " " << plus << " " << shift
                          << "', reg: '" << reg << "'" << std::endl;
            }

        } else if (input == "OR") {
            try {
                infile >> reg >> operand >> plus >> shift;
                if (reg[reg.size() - 1] != ',') {
                    throw std::invalid_argument("Missing comma");
                }
                if (plus != "|") {
                    throw std::invalid_argument("Missing '|'");
                }
                // TODO Сделать проверку регистров и тд
                regAddr = std::stoi(reg.substr(1, reg.size() - 2));
                addr = std::stoi(operand.substr(1, operand.size() - 2));
                offset = std::stoi(shift.substr(1, shift.size() - 1));

                bitwiseOr(regAddr, addr, offset);
                logfile << "- type: OR" << std::endl;
                logfile << "  A: " << 74 << std::endl;
                logfile << "  B: " << std::endl;
                logfile << "    value: " << regAddr << std::endl;
                logfile << "  C: " << std::endl;
                logfile << "    value: " << addr << std::endl;
                logfile << "  D: " << std::endl;
                logfile << "    value: " << offset << std::endl;
            } catch (std::invalid_argument &e) {
                std::cerr << "Syntax error. Bitwise or failed. " << inputFile << "\n" << e.what() << std::endl;
                std::cerr << "input: '" << input << "', operand: '" << operand + " " << plus + " " << shift
                          << "', reg: '" << reg << "'" << std::endl;
                return;
            } catch (...) {
                std::cerr << "Syntax error. Bitwise or failed. " << inputFile << std::endl;
                std::cerr << "input: '" << input << "', operand: '" << operand << " " << plus << " " << shift
                          << "', reg: '" << reg << "'"
                  << std::endl;
      }
    }
  }

  infile.close();
  logfile.close();
}

Assemble::~Assemble() { os.close(); }