/*
 * The MIT License (MIT)
 *
 * Copyright (c) 2015 ThundeRatz
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

/*
 * Base trainer that sends kick off commands and lets the game play freely.
 */

#include <rcsc/trainer/trainer_command.h>
#include <rcsc/net/udp_socket.h>

#include <chrono>
#include <regex>
#include <sstream>
#include <thread>

namespace {
    void sendTrainerCommand(rcsc::UDPSocket& socket, const rcsc::TrainerCommand& command) {
        std::ostringstream ss;
        command.toStr(ss);
        const std::string& data = ss.str();
        socket.send(data.c_str(), data.size());
    }

    void freeplay_trainer() {
        static char buf[1024];
        int half_time_duration = 0;
        rcsc::UDPSocket sock("127.0.0.1", 6001);

        sendTrainerCommand(sock, rcsc::TrainerInitCommand(7));
        sendTrainerCommand(sock, rcsc::TrainerKickOffCommand());

        for (;;) {
            ssize_t length;

            std::this_thread::sleep_for(std::chrono::seconds(1));

            sendTrainerCommand(sock, rcsc::TrainerCheckBallCommand());
            while ((length = sock.receive(buf, sizeof(buf))) > 0) {
                // Remove null terminator
                if (!buf[length - 1])
                    length--;
                std::string message(buf, length);

                static const std::regex regex_command("\\((\\S+) (.*)\\)", std::regex_constants::optimize);
                std::smatch match;

                if (std::regex_match(message, match, regex_command)) {
                    const std::string& command(match[1]);
                    const std::string& arguments(match[2]);
                    if ((command == "init" && arguments == "ok") || command == "player_param" ||
                            command == "player_type")
                        continue;
                    if (match[1] == "ok") {
                        if (match[2] == "start")
                            continue;
                        static const std::regex regex_check_ball("check_ball (\\d+) [\\S_]+",
                                                                 std::regex_constants::optimize);
                        std::smatch game_time_match;

                        if (std::regex_match(arguments, game_time_match, regex_check_ball)) {
                            if (!half_time_duration)
                                throw std::runtime_error("check_ball received before server_param");
                            if (std::stoi(game_time_match[1]) == half_time_duration) {
                                std::cout << "Reached half time, sendind kick off\n";
                                sendTrainerCommand(sock, rcsc::TrainerKickOffCommand());
                            }
                            continue;
                        }
                    }
                    if (command == "server_param") {
                        static const std::regex regex_half_time("(-?[\\d\\.]+ ){69}([\\d]+)( -?[\\d\\.]+)+",
                                                                std::regex_constants::optimize);
                        std::smatch half_time_match;
                        if (std::regex_match(arguments, half_time_match, regex_half_time)) {
                            half_time_duration = std::stoi(half_time_match[2]);
                            std::cout << "Half time duration: " << half_time_duration << "\n";
                            continue;
                        }
                    }
                }

                throw std::runtime_error("Invalid message " + message);
            }
        }
    }
}  // namespace

int main() {
    freeplay_trainer();
    return 0;
}
