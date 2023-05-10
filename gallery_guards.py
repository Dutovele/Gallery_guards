
num_guards = 0
num_intervals = 0

guard_names = []
halls = []
offers = []

guard_containter = []
guard_dic = {}

gallery_times_1=[]
gallery_times_2=[]

gallery_times_1_summed = []
gallery_times_2_summed = []
guard_conflict_times = []

free_gal_1 = 0
free_gal_2 = 0

opening_time_min = 600

class Guard:
    global halls
    global gallery_times_1
    global gallery_times_2
    global guard_conflict_times

    def __init__(self, id,name):
        self.id = id
        self.times_h1 = []
        self.times_h2 = []
        self.summed_times1 = []
        self.summed_times2 = []
        self.name = name
        self.conflict_time = 0

    def add_time(self, hall_name, stH, stM, enH, enM):
        start = normalised_times(stH, stM)
        end = normalised_times(enH, enM)
        if hall_name == halls[0]:
            self.times_h1.append([start, end])
        else:
            self.times_h2.append([start, end])

    def load_summed_times(self):
        for time in self.summed_times1:
            gallery_times_1.append(time)
        for time in self.summed_times2:
            gallery_times_2.append(time)

    def sort_times(self):
        self.times_h1.sort()
        self.times_h2.sort()

    def cal_summed_times(self):
        if self.times_h1 != [] and self.times_h2 != []:
            self.summed_times1 = summing_times(self.times_h1)
            self.summed_times2 = summing_times(self.times_h2)


    def count_conflict(self):
        global guard_containter

        for i in range(len(self.summed_times1)):
            starttime1 = self.summed_times1[i][0]
            endtime1 = self.summed_times1[i][1]
            for j in range(len(self.summed_times2)):
                starttime2 = self.summed_times2[j][0]
                endtime2 = self.summed_times2[j][1]
                self.conflict_time += get_conflict_time(starttime1, starttime2, endtime1, endtime2)

        guard_conflict_times.append([min_to_hours(self.conflict_time),self.name])


def summing_times(times):
    count = 0
    sum_interval = []
    top = times[0][0]
    bot = times[0][1]

    for i in range(len(times)):

        if i + 1 == len(times):
            interval = [top, bot]
            sum_interval.append(interval)
            break
        next_top = times[i + 1][0]
        next_bot = times[i + 1][1]

        if top <= next_top and bot <= next_bot and next_top <= bot:
            if bot <= next_bot:
                bot = next_bot
            else:
                bot = times[i][1]

        elif next_top > bot and next_bot >= next_top:
            interval = [times[count][0], bot]
            sum_interval.append(interval)
            count = i + 1
            top = next_top
            bot = next_bot
            if i + 1 == len(times):
                break

    return sum_interval

def summing_times2(times):
    count = 0
    sum_interval = []
    top = times[0][0]
    bot = times[0][1]

    for i in range(len(times)):

        if i + 1 == len(times):
            interval = [top, bot]
            sum_interval.append(interval)
            break
        next_top = times[i + 1][0]
        next_bot = times[i + 1][1]

        if top <= next_top and bot <= next_bot and next_top-1 <= bot:
            if bot <= next_bot:
                bot = next_bot
            else:
                bot = times[i][1]

        elif next_top >= bot and next_bot >= next_top:
            interval = [times[count][0], bot]
            sum_interval.append(interval)
            count = i + 1
            top = next_top
            bot = next_bot
            if i + 1 == len(times):
                break

    return sum_interval

def caluclate_confilicts():
    global guard_containter
    global gallery_times_1_summed
    global gallery_times_2_summed
    global gallery_times_1
    global gallery_times_2

    for g in guard_containter:
        # print("Sorting Guard:",g.name)
        g.sort_times()
        g.cal_summed_times()

    for g in guard_containter:
        # print("Getting Conflict Guard:", g.name)
        g.count_conflict()
        g.load_summed_times()
    # print(gallery_times_1)
    # print(gallery_times_2)
    gallery_times_1.sort()
    gallery_times_2.sort()
    gallery_times_1_summed = summing_times(gallery_times_1)
    gallery_times_2_summed = summing_times(gallery_times_2)


def get_inputs():
    global num_guards
    global num_intervals
    global guard_names
    global halls
    global offers
    global guard_dic
    global guard_containter

    num_guards, num_intervals = input().split(",")
    num_guards = int(num_guards)
    num_intervals = int(num_intervals)

    templine = input().strip("\n")
    guard_names = templine.split(", ")
    for i in range(len(guard_names)):

        temp_gaurd_obj = Guard(len(guard_containter), guard_names[i])
        guard_containter.append(temp_gaurd_obj)
        guard_dic[guard_names[i]] = len(guard_containter) - 1

    templine = input().strip("\n")
    halls = templine.split(", ")

    for i in range(num_intervals):
        templine = input().strip("\n")
        templine2 = templine.split(", ")
        guard_id = guard_dic[templine2[0]]
        guard_obj = guard_containter[guard_id]
        start_time = templine2[1].split(":")
        start_time_h = int(start_time[0])
        start_time_m = int(start_time[1])
        end_time = templine2[2].split(":")
        end_time_h = int(end_time[0])
        end_time_m = int(end_time[1])
        guard_obj.add_time(templine2[3],start_time_h, start_time_m, end_time_h, end_time_m)


def normalised_times(hour, minute):
    norm_time_min = hours_to_min(hour, minute) - 480
    return norm_time_min


def hours_to_min(hours, minutes):
    time_in_min = int(hours*60 + minutes)
    return time_in_min


def min_to_hours(minutes):

    time_in_hours = int(minutes//60)
    time_in_min = int(minutes%60)
    if len(str(time_in_hours)) == 1:
        time_in_hours = "0"+str(time_in_hours)
    else:
        time_in_hours = str(time_in_hours)
    if len(str(time_in_min)) == 1:
        time_in_min = "0"+str(time_in_min)
    else:
        time_in_min = str(time_in_min)
    return str(time_in_hours + ":" + time_in_min)


def get_conflict_time(starttime1, starttime2,endtime1,endtime2):
    conf_time = 0

    if starttime2 == starttime1 and endtime2 == endtime1:
        conf_time = endtime2-starttime2

    elif starttime2 > starttime1 and endtime2 < endtime1:
        conf_time = endtime2-starttime2

    elif starttime2 < starttime1 and endtime2 > endtime1:
        conf_time = endtime1 - starttime1

    elif starttime2 > starttime1 and endtime2 == endtime1:
        conf_time = endtime2-starttime2

    elif starttime2 < starttime1 and endtime2 == endtime1:
        conf_time = endtime2 - starttime1

    elif starttime2 == starttime1 and endtime2 < endtime1:
        conf_time = endtime2-starttime2

    elif starttime2 == starttime1 and endtime2 > endtime1:
        conf_time = endtime1 - starttime2

    elif starttime2>starttime1 and endtime2>endtime1 and endtime1 < starttime2:
        return 0

    elif starttime2<starttime1 and endtime2<endtime1 and endtime2 < starttime1:
        return 0

    elif starttime2<starttime1 and endtime2<endtime1:
        conf_time = endtime2 - starttime1

    elif starttime2>starttime1 and endtime2>endtime1:
        conf_time = endtime1 - starttime2
    return conf_time+1

def gaps_finder(sum_interval):

    free_time = 0
    count = 0
    free_interval = []
    top = sum_interval[0][0]
    bot = sum_interval[0][1]
    for i in range(len(sum_interval)):

        if i + 1 == len(sum_interval):
            break
        next_top = sum_interval[i + 1][0]
        next_bot = sum_interval[i + 1][1]

        if next_top <= bot and top <= next_top:
            # print("Keep going")

            if bot <= next_bot:
                bot = next_bot
            else:
                bot = sum_interval[i][1]

        elif next_top > bot and next_bot >= next_top:
            # print("FREE INTERVAL FOUND")

            free = [sum_interval[count][1],sum_interval[i+1][0]]
            free_interval.append(free)
            print(free[1] - free[0])
            free_time += (free[1] - free[0]-1)
            count = i + 1
            print("The free_interval is ", free)
            print("The free time now is ", free_time)

            if i + 1 == len(sum_interval):
                break
            top = next_top
            bot = next_bot


    if sum_interval[0][0] != 00 and sum_interval[-1][1] != 599:
        free_time += int(sum_interval[0][0])
        print("Adding the interval at the beginning + ", sum_interval[0][0])
        print("Free time now is: ", free_time)
        free_time += (599 - sum_interval[-1][1])
        print("Adding the end interval + ", (599 - sum_interval[-1][1]))
        print("Free time now is: ", free_time)

    return free_time

def free_times():
    global gallery_times_1_summed
    global gallery_times_2_summed
    global gallery_times_1
    global gallery_times_2
    global guard_conflict_times
    global free_gal_1
    global free_gal_2
    global opening_time_min

    print(gallery_times_1_summed)
    print(gallery_times_2_summed)


    time1_merged = summing_times2(gallery_times_1_summed)
    time2_merged = summing_times2(gallery_times_2_summed)

    print(time1_merged)
    print(time2_merged)

    free_gal_1 = gaps_finder(time1_merged)
    free_gal_2 = gaps_finder(time2_merged)

    print("{} {}".format(min_to_hours(free_gal_1), min_to_hours(free_gal_2)))
    guard_conflict_times.sort()

    for g in guard_conflict_times:
        print(g[0] + " " + g[1])

def gallery_times():
    global gallery_times_1_summed
    global gallery_times_2_summed
    global gallery_times_1
    global gallery_times_2
    global guard_conflict_times

    opening_time_min = 600

    print(gallery_times_1_summed)
    print(gallery_times_2_summed)
    g1_ocupied_min=0
    g2_ocupied_min=0

    count1=0
    count2=0
    for i in range(len(gallery_times_1_summed)):
        # if i > 0:
        g1_ocupied_min += 1


        if gallery_times_1_summed[i-1][1] == gallery_times_1_summed[i][0]-1 :
            # g1_ocupied_min += 1
            count1 += 1

        g1_ocupied_min += gallery_times_1_summed[i][1] - gallery_times_1_summed[i][0]

    print(count1)
    if len(gallery_times_1_summed)>2:
        g1_ocupied_min += count1
    for i in range(len(gallery_times_2_summed)):
        g2_ocupied_min += 1

        if gallery_times_2_summed[i-1][1] == gallery_times_2_summed[i][0]-1 :
            count2 += 1
        g2_ocupied_min += gallery_times_2_summed[i][1] - gallery_times_2_summed[i][0]
    print(count2)
    if len(gallery_times_2_summed)>2:
        g2_ocupied_min+= count2
    g1_unoc_min = opening_time_min - g1_ocupied_min
    g2_unoc_min = opening_time_min - g2_ocupied_min
    print("{} {}".format(min_to_hours(g1_unoc_min), min_to_hours(g2_unoc_min)))
    guard_conflict_times.sort()

    for g in guard_conflict_times:
        print(g[0]+" "+g[1])

def get_input_from_file(dir):
    global num_guards
    global num_intervals
    global guard_names
    global halls
    global offers
    global guard_dic
    global guard_containter

    line_number = 0

    file = open(dir,'r')
    for line in file:
        if line_number == 0:
            num_guards, num_intervals = line.split(",")
            num_guards = int(num_guards)
            num_intervals = int(num_intervals)
        elif line_number==1:
            templine = line.strip("\n")
            guard_names = templine.split(", ")
            # print(guard_names)
            for i in range(len(guard_names)):

                temp_gaurd_obj = Guard(len(guard_containter), guard_names[i])
                guard_containter.append(temp_gaurd_obj)
                guard_dic[guard_names[i]] = len(guard_containter) - 1

        elif line_number == 2:
            templine = line.strip("\n")
            halls = templine.split(", ")

        else:
            templine = line.strip("\n")
            templine2 = templine.split(", ")
            # print(templine2)
            guard_id = guard_dic[templine2[0]]
            guard_obj = guard_containter[guard_id]
            start_time = templine2[1].split(":")
            start_time_h = int(start_time[0])
            start_time_m = int(start_time[1])
            end_time = templine2[2].split(":")
            end_time_h = int(end_time[0])
            end_time_m = int(end_time[1])
            guard_obj.add_time(templine2[3],start_time_h, start_time_m, end_time_h, end_time_m)

        line_number+=1
    file.close()





# get_inputs()
# get_input_from_file("./datapub_GAURDS/pub05.in")
get_input_from_file("../../pubdata_gallery/pub05.in")
caluclate_confilicts()
# gallery_times()
free_times()
# gallery_times()



