import sys
maze_text, maze_health_text, health_time, output_text = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
maze = open(maze_text, "r")
maze_w_h = open(maze_health_text, "r")
output = open(output_text, "w")
maze_list = [list(line.rstrip("\n")) for line in maze.readlines()]
maze_health_list = [list(line.rstrip("\n")) for line in maze_w_h.readlines()]


def find(sf, l):
    for y in l:
        for x in y:
            if x == sf:
                return y.index(x), l.index(y)
    return False


f_x = find("F", maze_list)[0]
f_y = find("F", maze_list)[1]
s_x = find("S", maze_list)[0]
s_y = find("S", maze_list)[1]
f_x_h = find("F", maze_health_list)[0]
f_y_h = find("F", maze_health_list)[1]
s_x_h = find("S", maze_health_list)[0]
s_y_h = find("S", maze_health_list)[1]
start_health = health_time


def change(l):
    for i in range(len(l)):
        for n, k in enumerate(l[i]):
            if k != "S" and k != "F" and k != "1":
                l[i][n] = "0"


def path(x, y, m_list, health, h_situation):
    # base case
    try:
        if m_list[y][x] == "W" or m_list[y][x] == "2" or x < 0 or y < 0 or health < 0:
            return False
        if h_situation == "-":
            if x == f_x and y == f_y:
                return True
        if h_situation == "+":
            if x == f_x_h and y == f_y_h and health >= 0:
                return True
            if m_list[y][x] == "H":
                health = start_health
    except IndexError:
        return False
    # recursive case
    m_list[y][x] = "2"
    if h_situation == "-":
        if path(x-1, y, m_list, health, h_situation) or path(x, y-1, m_list, health, h_situation) or \
                path(x+1, y, m_list, health, h_situation) or path(x, y+1, m_list, health, h_situation) is True:
            m_list[y][x] = "1"
            return True
        return m_list[y][x] == "1"
    if h_situation == "+":
        if path(x - 1, y, m_list, health-1, h_situation) or path(x, y - 1, m_list, health-1, h_situation) or \
                path(x + 1, y, m_list, health-1, h_situation) or path(x, y + 1, m_list, health-1, h_situation) is True:
            if health > 0:
                m_list[y][x] = "1"
                return True
            return m_list[y][x] == "1"


path(s_x, s_y, maze_list, health_time, "-")
maze_list[s_y][s_x] = "S"
change(maze_list)
for line in maze_list:
    output.write(", ".join(line) + "\n")
output.write("\n")
path(s_x_h, s_y_h, maze_health_list, health_time, "+")
maze_health_list[s_y_h][s_x_h] = "S"
change(maze_health_list)
for line in maze_health_list:
    output.write(", ".join(line) + "\n")
output.close()
