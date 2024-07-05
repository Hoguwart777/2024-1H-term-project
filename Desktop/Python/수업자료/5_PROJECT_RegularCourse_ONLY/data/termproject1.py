import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import csv
import warnings
# 한글 폰트 설정
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
warnings.filterwarnings(action = 'ignore')

# file_name으로 받은 데이터를 가공하는 클래스
class sort_pandas:
    
    result_dataFrame = []
    
    def __init__(self, file_name, bus_number):
        self.file_name = file_name
        self.bus_number = bus_number
        
    def readfile(self):
        result_dataFrame = pd.read_csv(self.file_name, sep = ',', encoding = 'cp949')
        return result_dataFrame
    
    def bus_num_sortfile(self):
        filt_bus_number = (self.readfile()['노선번호'] == self.bus_number)
        return self.readfile()[filt_bus_number]
    
    def bus_num_and_station_sortfile(self):
        data = self.bus_num_sortfile()
        station_num = data['역명'].str.slice(-6, -1)
        data['정류장 번호'] = station_num
        result_dataFrame = data.sort_values('정류장 번호')
        return result_dataFrame
    
    def dataFile_colRemove(self):
        removeCol = ['노선명', '표준버스정류장ID', '버스정류장ARS번호','교통수단타입명', '등록일자', '정류장 번호']
        data = self.bus_num_and_station_sortfile()
        result_dataFrame = data.drop(columns = removeCol)
        return result_dataFrame
    
class TotalBusGraph(sort_pandas):
    
    hours = [f'{hour}시' for hour in range(24)]

    def __init__(self, file_name, bus_number):
        super().__init__(file_name, bus_number)
        self.bus_number_list = []
        df = self.readfile()['노선번호']
        for item in df:
            if(item not in self.bus_number_list):
                self.bus_number_list.append(item)
                
    def getTotalBusGraph(self, bus_number):
        matplotlib.rcParams['font.size'] = 10
        if(bus_number not in self.bus_number_list):
            print("해당하는 노선번호가 없습니다.")
        else:
            #데이터 선별
            data_list = []
            data_fix = self.dataFile_colRemove()
            Data = data_fix[data_fix.columns[2:77:3]]
            Data.reset_index(inplace = True)
            result_data = Data.drop(columns = ['index']).T
            for i in range(result_data.shape[0]):
                data_list.append(result_data.iloc[i])

            # 시간별 데이터에서 최댓값과 그에 해당하는 정류장 저장
            max_value_list = []
            station_name_list = []
            for List in data_list[1:]:
                max_value = 0
                station_name = ""
                for i in range(len(List)):
                    if(max_value < int(List[i])):
                        max_value = int(List[i])
                        station_name = data_list[0][i]
                max_value_list.append(max_value)
                station_name_list.append(station_name)
            
            # 꺾은선 그래프 그리기
            fig, ax1 = plt.subplots(figsize = (22, 12))
            ax2 = ax1.twinx()
            lns1 = ax1.plot(self.hours, data_list[1:], label = data_list[0], ls = '-.')
            lns2 = ax2.plot(self.hours, max_value_list, marker = 'o', mfc = '#a0c4ff')
            lns = lns1 + lns2
            labs = [l.get_label() for l in lns]
            ax1.legend(lns, labs ,ncol = 5, bbox_to_anchor = (0.5, -0.15), loc = 'upper center')

            for j in range(len(max_value_list)):
                ax2.annotate(f'{station_name_list[j]}\n{max_value_list[j]}명', xy = (self.hours[j], max_value_list[j]), 
                textcoords = 'offset points', xytext = (0,10), ha = 'center')
    
            ax1.grid()
            ax1.set_xlabel('시간')
            ax1.set_ylabel('승객 수')
            ax1.set_title(f'{bus_number}번 버스 교통량 그래프')
    
            ax2.set_ylabel('승객 수')
            return plt.show()


class Time_by_station_Graph(sort_pandas):

    hours = [f'{hour}시' for hour in range(24)]
    
    def __init__(self, file_name, bus_number):
        super().__init__(file_name, bus_number)
        self.bus_number_list = []
        df = self.readfile()['노선번호']
        for item in df:
            if(item not in self.bus_number_list):
                self.bus_number_list.append(item)
        
    def get_Time_by_station_Graph(self, index_number):
        # 데이터 선별
        if(self.bus_number not in self.bus_number_list):
            print("해당하는 노선번호가 없습니다")
        else:
            data_fix = self.dataFile_colRemove()
            Data = data_fix[data_fix.columns[2:77:3]]
            Data.reset_index(inplace = True)
            result_data = Data.drop(columns = ['index']).T

            # y값 선별
            y_axis_data = []
            for i in range(1, result_data.shape[0]):
                y_axis_data.append(result_data.iloc[i][index_number])

            bus_station = result_data.iloc[0][index_number]
            colors = [
                "#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF", "#FFB3BA",
                "#FFC0CB", "#FFD700", "#B0E0E6", "#F5DEB3", "#E6E6FA", "#D3D3D3",
                "#FFB6C1", "#F08080", "#E0FFFF", "#FAFAD2", "#D8BFD8", "#DDA0DD",
                "#B0C4DE", "#ADD8E6", "#98FB98", "#FF69B4", "#F4A460", "#D2B48C"
            ]

            # 데이터 레이블 표현
            matplotlib.rcParams['font.size'] = 10
            bar = plt.bar(self.hours, y_axis_data, color = colors)
            for idx,rect in enumerate(bar):
                plt.text(idx, rect.get_height() + 1, y_axis_data[idx], ha = 'center')
            plt.title(f'{self.bus_number}번의 {bus_station} 시간별 데이터')
            plt.xlabel('시간')
            plt.ylabel('이용객 수')
            plt.xticks(rotation = 90)
            return plt.show()

class Most_Passengers_graph_by_station(sort_pandas):
    
    hours = [f'{hour}시' for hour in range(24)]

    def __init__(self, file_name, bus_number):
        super().__init__(file_name, bus_number)
        self.bus_number_list = []
        df = self.readfile()['노선번호']
        for item in df:
            if(item not in self.bus_number_list):
                self.bus_number_list.append(item)

    def get_Most_Passengers_graph_by_station(self, bus_number):
        if(bus_number not in self.bus_number_list):
            print("해당하는 노선번호가 없습니다.")
        else:
            # 데이터 선별
            data_list = []
            data_fix = self.dataFile_colRemove()
            Data = data_fix[data_fix.columns[2:77:3]]
            Data.reset_index(inplace = True)
            result_data = Data.drop(columns = ['index'])
            for i in range(result_data.shape[0]):
                data_list.append(result_data.iloc[i])

            # 정류장별로 최댓값 추출과 그 당시의 시간대 추출
            max_value_list = []
            hour_list = []
            for List in data_list:
                max_value = 0
                station_name = ''
                for i in range(1, len(List)):
                    if(max_value < int(List[i])):
                        max_value = int(List[i])
                        hour = self.hours[i]
                max_value_list.append(max_value)
                hour_list.append(hour)

            # 정류장 분할
            division_of_data_num1 = (len(max_value_list) // 3)
            division_of_data_num2 = 2 * division_of_data_num1

            # 그래프 그리기
            plt.figure(figsize = (22, 40))
            matplotlib.rcParams['font.size'] = 18

            plt.subplot(311)
            plt.plot(result_data['역명'][:division_of_data_num1], max_value_list[:division_of_data_num1], marker = 'v')
    
            for j in range(division_of_data_num1):
                plt.annotate(f'{hour_list[j]}\n{max_value_list[j]}명', xy = (result_data['역명'][j], max_value_list[j]),
                        textcoords = 'offset points', xytext = (0, 10), ha = 'center')
            
            plt.xlabel('정류장')
            plt.ylabel('승객 수')
            plt.xticks(rotation = 90)
            plt.grid()
    
            plt.subplot(312)
            plt.plot(result_data['역명'][division_of_data_num1:division_of_data_num2],
                max_value_list[division_of_data_num1:division_of_data_num2], marker = 'X')
    
            for k in range(division_of_data_num1, division_of_data_num2):
                plt.annotate(f'{hour_list[k]}\n{max_value_list[k]}명', xy = (result_data['역명'][k], max_value_list[k]),
                    textcoords = 'offset points', xytext = (0, 10), ha = 'center')
                      
            plt.xlabel('정류장')
            plt.ylabel('승객 수')
            plt.xticks(rotation = 90)
            plt.grid()
    
            plt.subplot(313)
            plt.plot(result_data['역명'][division_of_data_num2:], max_value_list[division_of_data_num2:], marker = '*')
    
            for l in range(division_of_data_num2, len(max_value_list)):
                plt.annotate(f'{hour_list[l]}\n{max_value_list[l]}명', xy = (result_data['역명'][l], max_value_list[l]),
                    textcoords = 'offset points', xytext = (0, 10), ha = 'center')
                      
            plt.xlabel('정류장')
            plt.ylabel('승객 수')
            plt.xticks(rotation = 90)
            plt.grid()
    
            plt.tight_layout()
            return plt.show()
        
#file_name을 받아서, 받은 파일의 데이터의 일부를 list로 반환하는 클래스
class fileRead:

    def __init__(self, file_name):
        self.file_name = file_name

    def file_open(self):
        data = list()
        file = open(self.file_name, 'r', encoding = 'utf-8')
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
        file.close()
        return data
    
    def data_correct(self):
        data_correct2 = []
        data_correct1 = self.file_open()[1:]
        for i in range(len(data_correct1)):
            data_correct2.append([data_correct1[i][6], data_correct1[i][13:]])
        return data_correct2        
        
class Data_5100(fileRead):

    def __init__(self, file_name):
        super().__init__(file_name)

    def get_5100_graph(self):
        # 데이터 가공
        data_5100 = self.data_correct()
        data_5100_list = data_5100[2:]

        # x값 데이터와 y값 데이터 추출
        x_axis_data = []
        y_axis_data = []
        for i in range(len(data_5100_list)):
            data_5100_list[i][0] = data_5100_list[i][0][0:3]
            x_axis_data.append(data_5100_list[i][0])
            y_axis_data.append(int(data_5100_list[i][1][2]))

        # y값의 최댓값 구하기
        max_value = 0
        for item in y_axis_data:
            if(max_value <= item):
                max_value = item

        # 그래프 그리기
        matplotlib.rcParams['font.size'] = 10
        colors = ['#ffadad' if item != max_value else '#9bf6ff' for item in y_axis_data]
        bar = plt.bar(x_axis_data, y_axis_data, color = colors)

        for idx, rect in enumerate(bar):
            plt.text(idx, rect.get_height() + 1, y_axis_data[idx], ha = 'center')
        plt.title('5100번 버스 3월 승하차량 데이터')
        plt.xlabel('시간')
        plt.ylabel('승객 수')
        plt.xticks(rotation = 90)
        return plt.show()
    
userInput_bus_number = input('버스의 노선번호를 입력해주세요 : ')
tbg = TotalBusGraph('Seoul_bus_2024_03_fix.csv', userInput_bus_number)
tbg.getTotalBusGraph(userInput_bus_number)

userInput_index_number = int(input("정류장의 인덱스 번호를 입력해주세요 : "))
tbsg = Time_by_station_Graph('Seoul_bus_2024_03_fix.csv', userInput_bus_number)
tbsg.get_Time_by_station_Graph(userInput_index_number)

userInput_bus_number = input("버스의 노선번호를 입력해주세요 : ")
mpgbs = Most_Passengers_graph_by_station('Seoul_bus_2024_03_fix.csv', userInput_bus_number)
mpgbs.get_Most_Passengers_graph_by_station(userInput_bus_number)

num_5100_data = Data_5100('5100_bus_2024_03.csv')
num_5100_data.get_5100_graph()
