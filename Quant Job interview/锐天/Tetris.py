# Author : zhenghao
# Time : 2020/2/15 14:59
# File : Tetris.py
# Ide : PyCharm
# email: hao_zheng1997@163.com
import seaborn
import matplotlib.pyplot as plt



"""方块类，包括方块的形状定义和旋转方法"""
class tetromino:
    def __init__(self,shape,column,angle):
        self.shape = shape
        self.angle = angle
        self.column = column
        #为了统一定义，我们以0°状态方块最左下角(先最左，再最下)的点为原点，定义每个方块的相对坐标
        self.shape_dict = {
            'I':[[0,0],[1,0],[2,0],[3,0]],
            'J':[[0,0],[0,1],[1,0],[2,0]],
            'L':[[0,0],[1,0],[2,0],[2,1]],
            'O':[[0,0],[1,0],[0,1],[1,1]],
            'S':[[0,0],[1,0],[1,1],[2,1]],
            'T':[[0,0],[1,0],[2,0],[1,1]],
            'Z':[[0,0],[1,0],[1,-1],[2,-1]],
        }
        self.rotate_coordinate = self.rotate()

    #定义旋转方法，为了方便计算，我们先按照原点旋转
    def rotate(self):
        #初始化结果
        after_rotate = self.shape_dict[self.shape]
        # 90°旋转（x,y）->(y,-x)
        if self.angle==90:
            for coordinate in after_rotate:
                coordinate[0],coordinate[1] = coordinate[1],-coordinate[0]
        # 180°旋转 (x,y) ->(-x,-y)
        if self.angle==180:
            for coordinate in after_rotate:
                coordinate[0],coordinate[1] = -coordinate[0],-coordinate[1]
        # 270°旋转 (x,y)->(-y,x)
        if self.angle==270:
            for coordinate in after_rotate:
                coordinate[0],coordinate[1] = -coordinate[1],coordinate[0]

        #调整坐标，找到先最左，再最下的坐标作为新的原点,方便我们放进方块时以最左边的方块为起点考虑
        def compare(a,b):
            if a[0]>b[0]:
                return True
            elif a[0]<b[0]:
                return False
            else:
                return a[1]>b[1]

        ## 冒泡排序找到我们想要的新原点
        for i in range(len(after_rotate)):
            for j in range(len(after_rotate)-i-1):
                if compare(after_rotate[j],after_rotate[j+1]):
                    after_rotate[j],after_rotate[j+1] = after_rotate[j+1],after_rotate[j]

        shift_x = 0-after_rotate[0][0]
        shift_y = 0-after_rotate[0][1]
        for k in range(len(after_rotate)):
            after_rotate[k][0]+=shift_x
            after_rotate[k][1]+=shift_y

        return after_rotate



"""游戏类，执行整个游戏过程"""
class Tetris:

    def __init__(self,width,tetromino,height,plot_mode):
        self.plotmode = plot_mode
        self.max_height = height #由于无高度假设，这里用一个大值表示>30000*4=120000即可
        self.width = width
        self.tetromino = tetromino
        self.map = [[0]*self.width for _ in range(self.max_height)]
        self.grade = 0
        self.grade_dict = {
            0: 0,
            1: 100,
            2: 250,
            3: 400,
            4: 1000,
        }
        self.ith_column_height = [0]*width   #记录每一列存在的最大高度


    def run(self):
        """加载方块"""
        plt.ion()
        for tetromino in self.tetromino:
            column = tetromino.column
            coordinate = tetromino.rotate_coordinate

            """放置方块，包含碰撞探测"""
            is_success = self.place_teromino(column,coordinate)
            if not is_success:
                return

            if self.plotmode:
                seaborn.heatmap(self.map,square=True)
                plt.show()
                plt.pause(1)
                plt.close()

            """检测消除，累计分数"""
            eliminate_line = self.eliminate_detect()

            if self.plotmode:
                seaborn.heatmap(self.map,square=True)
                plt.show()
                plt.pause(1)
                plt.close()

            self.grade+=self.grade_dict[eliminate_line]

        return self.grade,self.ith_column_height


    def place_teromino(self,column,coordinate):
        height = self.ith_column_height[column]
        core_coordinate_x = self.max_height - 1 - height
        core_coordinate_y = column
        """检测能否放下无冲突,冲突则往上移动一格，直到无冲突确定原点所在位置"""
        while 1:
            flag = 0
            for item in coordinate:
                temp_x = core_coordinate_x-item[1]
                temp_y = core_coordinate_y+item[0]

                if temp_y<0 or temp_y>=self.width:
                    print("the input tetromino can't place into the map!!!")  ## 错误输入，即超过宽度
                    return False

                if temp_x>=self.max_height or self.map[temp_x][temp_y] == 1 :  # 该处已经有方块或者超出底部
                    core_coordinate_x-=1
                    flag=1
                    break
            if flag:
                continue
            else:
                break

        """放置方块并且更新高度记录数组"""
        for item in coordinate:
            temp_x = core_coordinate_x-item[1]
            temp_y = core_coordinate_y+item[0]
            self.map[temp_x][temp_y] = 1
            self.ith_column_height[temp_y] = max(self.ith_column_height[temp_y],self.max_height-temp_x)
        return True

    def eliminate_detect(self):
        count = 0
        eliminate_list = []
        """扫描范围选取最大高度即可"""
        max_height = max(self.ith_column_height)
        for i in range(self.max_height-1,self.max_height-max_height-1,-1):
            flag = 1
            for j in range(self.width):
                if self.map[i][j]!=1:
                    flag = 0
            if flag:
                count+=1
                eliminate_list.append(i)  #记录哪一行被消除了

        for row in eliminate_list:
            self.map.pop(row)
            self.max_height-=1
            for i in range(len(self.ith_column_height)):
                self.ith_column_height[i]-=1

        return count


if __name__ == '__main__':
    plot_mode = 1 #默认开启画图模式，为了画图方便，在开启画图模式时，会将高度值设置较小,因此请考虑输入较少得方块
    height = 30 if plot_mode else 120001  #>30000*4即可
    text_loading = 1 ##默认txt文件读入数据，也可以改成0后变成人机交互模式,

    """交互形式输入"""
    if text_loading:
        with open("test.txt", 'r') as file:
            data = file.readlines()
        testcase = int(data[0])
        lines = 1
        for k in range(1, testcase + 1):
            width = int(data[lines].split(" ")[0])
            number = int(data[lines].split(" ")[1])
            lines += 1
            tetrominoes = []
            for j in range(number):
                shape_info = data[lines].split(" ")[0]
                column_info = int(data[lines].split(" ")[1])
                angle_info = int(data[lines].split(" ")[2])
                tetrominoes.append(tetromino(shape_info, column_info, angle_info))
                lines += 1
            game = Tetris(width, tetrominoes, height, plot_mode)
            score, ith_height = game.run()
            print(f"Case #{k}:")
            print(score)
            for i in ith_height:
                print(i, end=' ')
            print()

    else:
        testcase = int(input("please input your test case: "))
        for k in range(1,testcase+1):
            parameters = input("please input width and number, splited by space：")
            width = int(parameters.split(" ")[0])
            number = int(parameters.split(" ")[1])
            tetrominoes = []
            for i in range(number):
                tetromino_parameters = input("please input information for tetromino, splited by space: ")
                shape_info = tetromino_parameters.split(" ")[0]
                column_info = int(tetromino_parameters.split(" ")[1])
                angle_info = int(tetromino_parameters.split(" ")[2])
                tetrominoes.append(tetromino(shape_info,column_info,angle_info))
            game = Tetris(width,tetrominoes,height,plot_mode)
            score,ith_height = game.run()
            print(f"Case #{k}:")
            print(score)
            for i in ith_height:
                print(i,end=' ')
            print()


























