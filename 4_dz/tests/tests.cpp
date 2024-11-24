#include <gtest/gtest.h>
#include "Assemble.h"
#include "Interpret.h"

TEST(Assemble, Assembler_load) {
    std::ofstream input("test_input.asm");
    input << "LOAD_CONSTANT R4, #187";
    input.close();
    Assemble("test_input.asm", "test_output.bin", "test_log.csv");
    std::ifstream output("test_output.bin");
    unsigned char byte;

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0xc3);

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0xdc);

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x05);

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x00);

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x00);

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x00);

    std::remove("test_input.asm");
    std::remove("test_output.bin");
    std::remove("test_log.csv");
}

TEST(Assemble, Assembler_Read) {
    std::ofstream input("test_input.asm");
    input << "MEMORY_READ R5, [R4]";
    input.close();
    Assemble("test_input.asm", "test_output.bin", "test_log.csv");
    std::ifstream output("test_output.bin");
    unsigned char byte;

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x53);

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x2c);

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x00);

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x00);

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x00);
    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x00);

    std::remove("test_input.asm");
    std::remove("test_output.bin");
    std::remove("test_log.csv");
}

TEST(Assemble, Assembler_Write) {
    std::ofstream input("test_input.asm");
    input << "MEMORY_WRITE [R1 + 144], R6";
    input.close();
    Assemble("test_input.asm", "test_output.bin", "test_log.csv");
    std::ifstream output("test_output.bin");
    unsigned char byte;

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x35);

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x86);

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x14);

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x00);

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x00);

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x00);

    std::remove("test_input.asm");
    std::remove("test_output.bin");
    std::remove("test_log.csv");
}

TEST(Assemble, Assembler_Or) {
    std::ofstream input("test_input.asm");
    input << "OR R5, [491] | R1";
    input.close();
    Assemble("test_input.asm", "test_output.bin", "test_log.csv");
    std::ifstream output("test_output.bin");
    unsigned char byte;

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x4a);

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x5d);

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x0f);

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x00);

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x40);

    output.read(reinterpret_cast<char *>(&byte), sizeof(byte));
    EXPECT_EQ(byte, 0x00);

    std::remove("test_input.asm");
    std::remove("test_output.bin");
    std::remove("test_log.csv");
}
