import os
import re
import sys
import copy
from datetime import date
from datetime import datetime
from calendar import monthrange

# region 전역 변수
id_num = 0


# region 문자열 처리 함수
def strip_whitespace_0(s: str) -> str:
    """
    문자열 앞뒤의 공백열0을 제거
    개행(\n, \r)은 제거하지 않음
    """
    return s.strip(" \t\f\v")


def split_whitespace_1(s: str, maxsplit: int = 0) -> list[str]:
    """
    문자열을 공백열1 기준으로 나눔
    개행(\n, \r)은 제거하지 않음
    """
    return re.split(r"[ \t\f\v]+", s, maxsplit=maxsplit)


def remove_tail_letter(s: str, letter: str) -> str:
    """
    문자열 끝에 특정 문자가 붙어 있으면 제거(년, 월, 일 등)
    """
    if s.endswith(letter):
        return s[:-1]
    return s


# endregion


# region 데이터 요소 클래스
class Year:
    def __init__(self, s: str):
        self.value = self._parse(s)

    def _parse(self, s: str) -> int:
        s = remove_tail_letter(s, "년")
        if not re.fullmatch(r"[0-9]{1,4}", s):
            raise ValueError(
                "년은 1개 이상 4개 이하의 숫자, 이후 추가적인 '년' 문자로 이루어져야 합니다."
            )
        n = int(s)
        if not (1 <= n <= 9999):
            raise ValueError("년은 1~9999 사이여야 합니다.")
        return n

    def __str__(self):
        return f"{self.value}년"


class Month:
    def __init__(self, s: str):
        self.value = self._parse(s)

    def _parse(self, s: str) -> int:
        s = remove_tail_letter(s, "월")
        if not re.fullmatch(r"[0-9]{1,2}", s):
            raise ValueError(
                "월은 1개 혹은 2개의 숫자, 이후 추가적인 '월' 문자로 이루어져야 합니다."
            )
        n = int(s)
        if not (1 <= n <= 12):
            raise ValueError("월은 1~12 사이여야 합니다.")
        return n

    def __str__(self):
        return f"{self.value:02d}월"


class Day:
    def __init__(self, s: str):
        self.value = self._parse(s)

    def _parse(self, s: str) -> int:
        s = remove_tail_letter(s, "일")
        if not re.fullmatch(r"[0-9]{1,2}", s):
            raise ValueError(
                "일은 1개 혹은 2개의 숫자, 이후 추가적인 '일' 문자로 이루어져야 합니다."
            )
        n = int(s)
        if not (1 <= n <= 31):
            raise ValueError("일은 1~31 사이여야 합니다.")
        return n

    def __str__(self):
        return f"{self.value:02d}일"


class Date:
    """
    <년><날짜구분자><월><날짜구분자><일>
    <년><월><일>: '년', '월', '일' 문자 포함
    """

    def __init__(self, s: str):
        self.year, self.month, self.day = self._parse(s)
        self._validate_date()

    def _parse(self, s: str):
        if "/" in s or "-" in s:
            parts = re.split(r"[-/]", s)
            if len(parts) != 3:
                raise ValueError(
                    f"날짜 형식이 잘못되었습니다. 날짜구분자가 있을 경우 년, 월, 일이 날짜구분자에 의해 구분되어야 합니다. (입력: {s})"
                )

            try:
                year = Year(parts[0])
                month = Month(parts[1])
                day = Day(parts[2])
                return year, month, day
            except ValueError as e:
                raise ValueError(f"날짜 부분 값 오류: {e} (입력: {s})")

        elif "년" in s and "월" in s and "일" in s:
            match = re.fullmatch(r"([0-9]{1,4})년([0-9]{1,2})월([0-9]{1,2})일", s)

            if not match:
                raise ValueError(
                    f"날짜 형식이 잘못되었습니다. 날짜구분자가 없을 경우 년, 월, 일이 순서대로 나열되어야 합니다. (입력: {s})"
                )

            parts = match.groups()

            try:
                year = Year(parts[0])
                month = Month(parts[1])
                day = Day(parts[2])
                return year, month, day
            except ValueError as e:
                raise ValueError(f"날짜 부분 값 오류: {e} (입력: {s})")

        else:
            raise ValueError(
                "날짜구분자 (-, /) 또는 한글 단위 (년, 월, 일) 모두를 포함해야 합니다."
            )

    def _validate_date(self):
        try:
            date(self.year.value, self.month.value, self.day.value)
        except:
            raise ValueError(
                f"날짜가 현행 그레고리력에 포함되지 않습니다. (날짜: {self})"
            )

    def __str__(self):
        return f"{self.year}/{self.month}/{self.day}"


class Hour:
    def __init__(self, s: str):
        self.value = self._parse(s)

    def _parse(self, s: str) -> int:
        s = remove_tail_letter(s, "시")
        if not re.fullmatch(r"[0-9]{1,2}", s):
            raise ValueError(
                "시는 1개 혹은 2개의 숫자, 이후 추가적인 '시' 문자로 이루어져야 합니다."
            )
        n = int(s)
        if not (0 <= n <= 23):
            raise ValueError("시는 0~23 사이여야 합니다.")
        return n

    def __str__(self):
        return f"{self.value:02d}"


class Minute:
    def __init__(self, s: str):
        self.value = self._parse(s)

    def _parse(self, s: str) -> int:
        s = remove_tail_letter(s, "분")
        if not re.fullmatch(r"[0-9]{1,2}", s):
            raise ValueError(
                "분은 1개 혹은 2개의 숫자, 이후 추가적인 '분' 문자로 이루어져야 합니다."
            )
        n = int(s)
        if not (0 <= n <= 59):
            raise ValueError("분은 0~59 사이여야 합니다.")
        return n

    def __str__(self):
        return f"{self.value:02d}"


class Time:
    """시:분"""

    def __init__(self, s: str):
        self.hour, self.minute = self._parse(s)
        self._validate_time()

    def _parse(self, s: str):
        if ":" in s:
            parts = s.split(":", 1)
            if len(parts) != 2:
                raise ValueError(
                    "시간 형식이 잘못되었습니다. ':' 문자를 사용할 경우 시, 분이 ':' 문자를 통해 구분되어야 합니다."
                )

            return Hour(parts[0]), Minute(parts[1])

        if "시" in s and "분" in s:
            match = re.fullmatch(r"([0-9]{1,2})시([0-9]{1,2})분", s)

            if not match:
                raise ValueError(
                    f"시간 형식이 잘못되었습니다. ':' 문자를 사용하지 않을 경우 년, 월, 일이 공백/구분자 없이 순서대로 나열되어야 합니다. (입력: {s})"
                )

            parts = match.groups()

            return Hour(parts[0]), Minute(parts[1])

        if "시" in s:
            match = re.fullmatch(r"([0-9]{1,2})시", s)

            if not match:
                raise ValueError(
                    f"시간 형식이 잘못되었습니다. '분' 문자를 사용하지 않고 '시' 문자만 사용 시 시간은 시 그 자체여야 합니다. (입력: {s})"
                )

            parts = match.groups()

            return Hour(parts[0]), Minute("0")

        if re.fullmatch(r"[0-9]{3,4}", s):
            if len(s) == 4:
                h = s[:2]
                m = s[2:]
            elif len(s) == 3:
                h = s[:1]
                m = s[1:]

            return Hour(h), Minute(m)

        return Hour(s), Minute("0")

    def _validate_time(self):
        if not (0 <= self.hour.value <= 23 and 0 <= self.minute.value <= 59):
            raise ValueError(f"시간은 0시0분 이상 23시59분 이하입니다.")

    def __str__(self):
        return f"{self.hour}:{self.minute}"


class DateTime:
    """<날짜> <시간>"""

    def __init__(self, s: str):
        self.date, self.time = self._parse(s)

    def _parse(self, s: str):
        parts = s.split(" ", 1)
        if len(parts) != 2:
            raise ValueError(
                "시각 형식이 잘못되었습니다. 시각은 날짜와 시간이 공백을 기준으로 나열되어 있어야 합니다. (입력: {s})"
            )
        return Date(parts[0]), Time(parts[1])

    def to_datetime(self) -> datetime:
        return datetime(
            self.date.year.value,
            self.date.month.value,
            self.date.day.value,
            self.time.hour.value,
            self.time.minute.value,
        )

    def __str__(self):
        return f"{self.date} {self.time}"


class Period:
    """<시각>~<시각>"""

    def __init__(self, s: str):
        self.start, self.end = self._parse(s)

    def _parse(self, s):
        start, end = s.split("~", 1)

        start_dt = DateTime(start)
        end_dt = DateTime(end)

        if start_dt.to_datetime() >= end_dt.to_datetime():
            raise ValueError(
                "기간 형식이 잘못되었습니다. 기간의 시작 시각은 끝 시각보다 빨라야 합니다. (입력 {s})"
            )

        return start_dt, end_dt

    def overlaps(self, other) -> bool:
        a1, a2 = self.start.to_datetime(), self.end.to_datetime()
        b1, b2 = other.start.to_datetime(), other.end.to_datetime()

        if a1 == b1:
            return True

        if a1 > b1:
            (a1, b1) = (b1, a1)
            (a2, b2) = (b2, a2)

        if a2 >= b1:
            return True

        return False

    def __str__(self):
        return f"{self.start}~{self.end}"


class Content:
    """길이 0 이상 개행을 포함하지 않고 첫/마지막 문자는 실상문자인 모든 문자열"""

    def __init__(self, s: str):
        self.value = s
        self._validate_content()

    def _validate_content(self):
        if "\n" in self.value or "\r" in self.value:
            raise ValueError("일정내용에 개행을 포함할 수 없습니다.")

        return True

    def __str__(self):
        return f"{self.value}"


class Schedule:
    """
    <기간>
    <기간><공백열1><일정내용>
    """

    def __init__(self, s: str):
        self.period, self.content = self._parse(s)
        self.number = -1
        self.schedule_id = 0
        self.repeat_id = 0
        self.allow_overlap = False
        self.repeat_type = None
        self.repeat_count = 0

    def _parse(self, s: str):
        parts = s.split(" ", 2)

        if len(parts) < 3:
            raise ValueError(
                "일정은 기간 그 자체이거나 기간과 일정내용이 공백열1을 경계로 하여 나열되어야 합니다."
            )

        sub_parts = split_whitespace_1(parts[-1], 1)

        if len(sub_parts) == 2:
            parts[2] = sub_parts[0]

            period = " ".join(parts)
            content = sub_parts[1]
        else:
            period = " ".join(parts)
            content = ""

        return Period(period), Content(content)

    def is_conflict(self, other: "Schedule") -> bool:
        """
        일정이 다른 일정과 충돌하는지 확인하는 함수
        """
        # 둘 중 하나라도 allow_overlap이 True일 경우 False 반환
        if self.allow_overlap or other.allow_overlap:
            return False

        # self의 기간과 other의 기간이 겹치는지 반환
        return self.period.overlaps(other.period)

    def __str__(self):
        if len(self.content.value) == 0:
            return f"{self.period}"
        else:
            return f"{self.period}\t{self.content}"


# class 일정시간 추가해야 합니다
class ScheduleTime:
    """
    일정시간. <년>, <년/월>, <날짜> 형식을 파싱하고 Period로 변환
    """

    def __init__(self, s: str):
        self._parse(s)

    def _parse(self, s: str):
        # <날짜> 그 자체 (년/월/일)
        try:
            temp_date = Date(s)
            self.year = temp_date.year
            self.month = temp_date.month
            self.day = temp_date.day
            self.mode = "day"
            return
        except ValueError:
            pass

        # <년><날짜구분자><월>
        try:
            parts = re.split(r"[-/]", s)
            if len(parts) == 2:
                self.year = Year(parts[0])
                self.month = Month(parts[1])
                self.day = None
                self.mode = "month"
                return
        except ValueError:
            pass

        # <년> 그 자체
        try:
            self.year = Year(s)
            self.month = None
            self.day = None
            self.mode = "year"
            return
        except ValueError:
            pass

        raise ValueError(f"일정시간 형식이 잘못되었습니다. (입력: {s})")

    def to_period(self) -> Period:
        """일정시간이 의미하는 기간을 Period 객체로 반환"""
        _year = self.year.value

        if self.mode == "day":
            # Day: 00:00 ~ 23:59
            _month = self.month.value
            _day = self.day.value
            start_dt_str = f"{_year}/{_month}/{_day} 00:00"
            end_dt_str = f"{_year}/{_month}/{_day} 23:59"

        elif self.mode == "month":
            # Month: Month/1 00:00 ~ Last day of Month 23:59
            _month = self.month.value
            _day_count = monthrange(_year, _month)[1]

            start_dt_str = f"{_year}/{_month}/1 00:00"
            end_dt_str = f"{_year}/{_month}/{_day_count} 23:59"

        elif self.mode == "year":
            # Year: Year/1/1 00:00 ~ Year/12/31 23:59
            start_dt_str = f"{_year}/1/1 00:00"
            end_dt_str = f"{_year}/12/31 23:59"

        else:
            raise ValueError("유효하지 않은 일정시간 모드입니다.")

        return Period(f"{start_dt_str}~{end_dt_str}")


class Repeater:
    """
    <반복유형><공백열1><반복횟수>
    """

    def __init__(self, base_schedule: Schedule, s: str):
        self.base_schedule = base_schedule
        self.repeat_type, self.repeat_count = self._parse(s)

    def _parse(self, s: str):
        parts = split_whitespace_1(s, 1)

        if len(parts) != 2:
            raise ValueError(f"Repeater: s({s}) is not splited to 2 parts")

        repeat_type = parts[0]
        repeat_count = parts[1]

        if (
            repeat_type != "M"
            and repeat_type != "m"
            and repeat_type != "Y"
            and repeat_type != "y"
        ):
            raise ValueError(f"repeat_type({repeat_type}) is not M, m, Y, y")

        try:
            repeat_count = int(repeat_count)
        except ValueError:
            raise ValueError(f"repeat_count({repeat_count}) is not Integer")

        if not (repeat_count >= 1 and repeat_count <= 999999):
            raise ValueError(f"repeat_count({repeat_count}) is not between 1~999,999")

        return repeat_type, repeat_count

    def can_repeat(self) -> bool:
        """
        반복자가 주어진 기준 일정의 기간과 반복 유형에서 반복이 가능한지 반환합니다
        """
        base_period = self.base_schedule.period

        base_start = base_period.start
        base_end = base_period.end

        tmp_year = base_start.date.year.value
        tmp_month = base_start.date.month.value
        tmp_day = base_start.date.day.value
        tmp_hour = base_start.time.hour.value
        tmp_minute = base_start.time.minute.value

        end_year = base_end.date.year.value
        end_month = base_end.date.month.value
        end_day = base_end.date.day.value
        end_hour = base_end.time.hour.value
        end_minute = base_end.time.minute.value

        count = 0

        if self.repeat_type == "M" or self.repeat_type == "m":
            count = 1
        elif self.repeat_type == "Y" or self.repeat_type == "y":
            count = 12

        tmp_year, tmp_month, tmp_day = self._get_next_date(
            tmp_year, tmp_month, tmp_day, count
        )

        if tmp_year != end_year:
            return tmp_year > end_year
        elif tmp_month != end_month:
            return tmp_month > end_month
        elif tmp_day != end_day:
            return tmp_day > end_day
        elif tmp_hour != end_hour:
            return tmp_hour > end_hour
        elif tmp_minute != end_minute:
            return tmp_minute > end_minute
        else:
            return False

    def get_repeat_schedules(self) -> list[Schedule]:
        """
        반복자의 기준 일정과 반복 유형, 반복 횟수에 따라 반복된 새로운 일정들을 반환합니다.
        """
        if not self.can_repeat():
            return None

        result_list = []

        base_period = self.base_schedule.period
        base_start = base_period.start
        base_end = base_period.end

        sy = base_start.date.year.value
        sm = base_start.date.month.value
        sd = base_start.date.day.value

        ey = base_end.date.year.value
        em = base_end.date.month.value
        ed = base_end.date.day.value

        count = 0

        if self.repeat_type == "M" or self.repeat_type == "m":
            count = 1
        elif self.repeat_type == "Y" or self.repeat_type == "y":
            count = 12

        for _ in range(self.repeat_count):
            sy, sm, sd = self._get_next_date(sy, sm, sd, count)
            ey, em, ed = self._get_next_date(ey, em, ed, count)

            if ey > 9999:
                break

            try:
                datetime(sy, sm, sd)
                datetime(ey, em, ed)
            except:
                # 현행 그레고리력에 포함되지 않음
                continue

            new_schedule = copy.deepcopy(self.base_schedule)

            new_schedule.period.start.date.year.value = sy
            new_schedule.period.start.date.month.value = sm
            new_schedule.period.start.date.day.value = sd

            new_schedule.period.end.date.year.value = ey
            new_schedule.period.end.date.month.value = em
            new_schedule.period.end.date.day.value = ed

            new_schedule.allow_overlap = self.base_schedule.allow_overlap
            new_schedule.repeat_id = self.base_schedule.schedule_id

            result_list.append(new_schedule)

        return result_list

    def _get_next_date(self, year: int, month: int, day: int, count: int):
        if type(count) is not int or count <= 0:
            raise ValueError(f"count({count}) is not positive integer")

        month += count

        while month > 12:
            month -= 12
            year += 1

        return year, month, day


# endregion


# region 데이터 파일
DATA_FILE = "schedule_data.txt"


def check_data_file() -> bool:
    """데이터 파일 존재 확인 및 생성"""
    if not os.path.exists(DATA_FILE):
        print("현재 경로에 데이터 파일이 없습니다.")
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                print("현재 경로에 빈 데이터 파일을 생성합니다 :")
                print(os.path.abspath(DATA_FILE))
                pass
        except PermissionError:
            print(
                "오류: 현재 경로에 데이터 파일 생성을 실패했습니다. 프로그램을 종료합니다."
            )

            return False

    if not os.access(DATA_FILE, os.R_OK | os.W_OK):
        print(os.path.abspath(DATA_FILE))
        print("에 대한 입출력 권한이 없습니다. 프로그램을 종료합니다.")

        return False

    return True


def load_schedules() -> list[Schedule]:
    """파일에서 일정 목록 불러오기"""
    schedules = []
    global id_num
    if not os.path.exists(DATA_FILE):
        return schedules
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n\r")
            if line:
                try:
                    parts = line.split("\t", 15)
                    if len(parts) != 16:
                        raise ValueError(
                            "데이터 파일이 형식에 맞지 않습니다. (line: {line})"
                        )
                    schedule = (
                        "/".join(parts[5:8])
                        + " "
                        + ":".join(parts[8:10])
                        + "~"
                        + "/".join(parts[10:13])
                        + " "
                        + ":".join(parts[13:15])
                        + " "
                        + parts[15]
                    )
                    sch = Schedule(schedule)
                    sch.allow_overlap = parts[0]
                    sch.schedule_id = parts[1]
                    sch.repeat_id = parts[2]
                    if parts[3] != "-":
                        sch.repeat_type = parts[3]
                    sch.repeat_count = parts[4]
                    schedules.append(sch)

                    id_num = max(id_num, int(parts[1]))
                except Exception as e:
                    print(f"[데이터 오류] {e}")
    sort_schedule(schedules)
    update_schedule_number(schedules)

    return schedules


def save_schedules(schedules: list[Schedule]):
    """일정 목록을 파일에 저장"""

    sort_schedule(schedules)
    update_schedule_number(schedules)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for sch in schedules:
            if sch.allow_overlap == "y":
                sch.allow_overlap = "Y"
            if sch.allow_overlap == "n":
                sch.allow_overlap = "N"
            if sch.repeat_type == "m":
                sch.repeat_type = "M"
            if sch.repeat_type == "y":
                sch.repeat_type = "Y"
            start = sch.period.start
            end = sch.period.end
            content = sch.content.value

            line = (
                f"{sch.allow_overlap}\t{sch.schedule_id}\t{sch.repeat_id}\t{sch.repeat_type}\t{sch.repeat_count}\t"
                f"{start.date.year.value}\t{start.date.month.value}\t{start.date.day.value}\t"
                f"{start.time.hour.value}\t{start.time.minute.value}\t"
                f"{end.date.year.value}\t{end.date.month.value}\t{end.date.day.value}\t"
                f"{end.time.hour.value}\t{end.time.minute.value}\t"
                f"{content}\n"
            )
            f.write(line)


# endregion


# region 명령어 리스트
delete_command_list = ["삭제", "ㅅㅈ", "delete", "d", "-"]
view_command_list = ["열람", "ㅇㄹ", "view", "v", "#"]
search_command_list = ["검색", "ㄱㅅ", "search", "s", "/"]
reschedule_command_list = ["조정", "ㅈㅈ", "reschedule", "r", "!"]
change_command_list = ["변경", "ㅂㄱ", "change", "c", "@"]
add_command_list = ["추가", "ㅊㄱ", "add", "a", "+"]
quit_command_list = ["종료", "ㅈㄹ", "quit", "q", "."]
period_command_list = ["반복", "ㅂㅂ", "period", "p", "&"]
# endregion

# region 명령어 함수


def add(schedules: list[Schedule], factor: str):
    try:
        new_schedule = Schedule(factor)
    except ValueError:
        print("오류: 추가 명령어의 인자인 일정을 다시 확인해 주십시오!")
        print("올바른 인자의 형태: <일정>")
        return

    mention = 1
    overlap = False
    for idx, sch in enumerate(schedules):
        if new_schedule.period.overlaps(sch.period):
            if mention:
                print("오류: 다음 일정과 기간이 겹칩니다!")
                mention = 0
            print("-> ", idx + 1, sch)
            overlap = True
    if not overlap:
        schedules.append(new_schedule)
        print("일정이 추가되었습니다!")
        save_schedules(schedules)
    return


def reschedule(schedules: list[Schedule], factor: str):
    if not factor:
        print("오류: 조정 명령어의 인자를 다시 확인해 주십시오!")
        print("올바른 인자의 형태: <일정번호> <공백열1> <기간>")
        return

    try:
        r_factors = split_whitespace_1(factor, 1)
        check = 1
        idx = int(r_factors[0]) - 1
        check = 0
        if idx < 0:
            print("오류: 일정번호에 양의 정수 값을 입력하세요!")
            return
        if idx >= len(schedules):
            print("오류: 입력한 일정번호에 해당하는 일정이 없습니다!")
            return
        if len(r_factors) < 2:
            print("오류: 조정 명령어의 인자인 기간을 다시 확인해 주십시오!")
            print("올바른 인자의 형태: <일정번호> <공백열1> <기간>")
            return

        r_sch = r_factors[1]
        schedule = schedules[idx]
        prev_number = schedule.number
        comsch = Schedule(r_sch)

        if comsch.content.value != "":
            print("오류: 조정 명령어의 인자인 기간을 다시 확인해 주십시오!")
            print("올바른 인자의 형태: <일정번호> <공백열1> <기간>")
            return

        overlap = False

        mention = 1
        for idx1, sch in enumerate(schedules):
            if comsch.period.overlaps(sch.period):
                if idx1 == idx:
                    continue
                if mention:
                    print("오류: 다음 일정과 기간이 겹칩니다!")
                    mention = 0
                print("-> ", idx1 + 1, sch)
                overlap = True

        if not overlap:
            schedule.period = comsch.period
            save_schedules(schedules)
            print("일정이 다음과 같이 조정되었습니다!")

            next_number = schedule.number

            same_order = prev_number == next_number

            if not same_order:
                print(
                    "(주의: 일정 순서의 변동으로 인해 해당 일정의 번호가 변경되었습니다!)"
                )
            for idx2, sch in enumerate(schedules):
                if sch.period.start.to_datetime() == comsch.period.start.to_datetime():
                    print(idx2 + 1, sch)
                    break
            return

    except ValueError:
        try:
            if check:
                if len(r_factors) != 2:
                    print("오류: 조정 명령어의 인자를 다시 확인해 주십시오!")
                    print("올바른 인자의 형태: <일정번호> <공백열1> <기간>")
                    return
                Schedule(r_factors[1])
                l = split_whitespace_1(r_factors[1], 3)
                if len(l) != 3:
                    print("오류: 조정 명령어의 인자를 다시 확인해 주십시오!")
                    print("올바른 인자의 형태: <일정번호> <공백열1> <기간>")
                    return
                print("오류: 조정 명령어의 인자인 일정번호를 다시 확인해 주십시오!")
                print("올바른 인자의 형태: <일정번호> <공백열1> <기간>")
            else:
                print("오류: 조정 명령어의 인자인 기간을 다시 확인해 주십시오!")
                print("올바른 인자의 형태: <일정번호> <공백열1> <기간>")
            return
        except ValueError:
            print("오류: 조정 명령어의 인자를 다시 확인해 주십시오!")
            print("올바른 인자의 형태: <일정번호> <공백열1> <기간>")
    except IndexError:
        print("오류: 조정 명령어의 인자인 기간을 다시 확인해 주십시오!")
        print("올바른 인자의 형태: <일정번호> <공백열1> <기간>")
        return


def change(schedules: list[Schedule], factor: str):
    if not factor:
        print("오류: 변경 명령어의 인자를 다시 확인해 주십시오!")
        print("올바른 인자의 형태: <일정번호> 혹은 <일정번호> <공백열1> <일정내용>")
        return
    try:
        c_factors = split_whitespace_1(factor, 1)
        idx = int(c_factors[0]) - 1
        content = None

        if idx < 0:
            print("오류: 일정번호에 양의 정수 값을 입력하세요!")
            return
        if idx >= len(schedules):
            print("오류: 입력한 번호에 해당하는 일정이 없습니다!")
            return
        if len(c_factors) == 2:
            content = c_factors[1]
        if not content:
            content = ""
        schedules[idx].content = Content(content)
        save_schedules(schedules)
        print("일정이 다음과 같이 변경되었습니다!")
        print(idx + 1, schedules[idx])
        return
    except ValueError:
        try:
            float_val = float(idx)
            print("오류: 일정번호에 양의 정수 값을 입력하세요!")
        except:
            print("오류: 일정번호에 문자가 올 수 없습니다!")
        return


def delete(schedules: list[Schedule], factor: str):
    if not factor:
        print("오류: 삭제 명령어의 인자인 일정번호를 다시 확인해 주십시오!")
        print("올바른 인자의 형태: <일정번호>")
        return

    if not schedules:
        print("기록된 일정이 없어 삭제할 수 없습니다!")
        return
        

    try:
        idx = int(factor) - 1

        if idx < 0:
            print("오류: 일정번호에 양의 정수 값을 입력하세요!")
            return
        if idx >= len(schedules):
            print("오류: 입력한 번호에 해당하는 일정이 없습니다!")
            return
        

        target = schedules[idx]

        current_repeat_id = 0
        if str(target.repeat_id).isdigit():
            current_repeat_id = int(target.repeat_id)

        current_schedule_id = 0
        if str(target.schedule_id).isdigit():
            current_schedule_id = int(target.schedule_id)

        is_repeat_schedule = current_repeat_id > 0 # [분기 1] 반복 일정 확인
        if is_repeat_schedule: 
            is_base_schedule = (current_repeat_id == current_schedule_id) # [분기 2] 기준 일정 확인
            if not is_base_schedule: 
                print("오류: 기준 일정의 일정번호로 다시 시도해 주십시오!")

                base_sch = None
                for sch in schedules:
                    check_sch_id = 0
                    if str(sch.schedule_id).isdigit():
                        check_sch_id = int(sch.schedule_id)

                    if check_sch_id == current_repeat_id:
                        base_sch = sch
                        break
                
                if base_sch:
                    print(f"기준 일정: {base_sch.number} {base_sch}")
                else:
                    print("(기준 일정을 찾을 수 없습니다.)")
                return

        # [서브 프롬프트]
        print(f"{target.number} {target}")

        while True:
            confirm = input("정말 삭제하시겠습니까? (Y/N)>>> ")
            confirm = confirm.upper()

            if confirm == "Y":
                if is_repeat_schedule: 
                    target_repeat_id = current_repeat_id
                    deleted_count = 0
                    
                    for i in range(len(schedules) - 1, -1, -1):
                        check_repeat_id = 0
                        if str(schedules[i].repeat_id).isdigit():
                            check_repeat_id = int(schedules[i].repeat_id)

                        if check_repeat_id == target_repeat_id:
                            schedules.pop(i)
                            deleted_count += 1
                            
                    print(f"반복 일정 그룹 {deleted_count}건이 모두 삭제되었습니다!")
                    
                else: 
                    schedules.pop(idx)
                    print(f"일정 [{target.number} {target}]이(가) 삭제되었습니다!")
                
                save_schedules(schedules)
                break
            elif confirm == "N":
                break
            else:
                print("오류: 인자가 잘못되었습니다!")

    except ValueError:
        if re.search(r"[^a-zA-Z0-9ㄱ-ㅎㅏ-ㅣ가-힣]", factor) is not None:
            print("오류: 인자에 기호가 올 수 없습니다!")
        else:
            print("오류: 인자에 문자가 올 수 없습니다!")

    except Exception as e:
        print(f"오류: 일정을 삭제하는 중 문제가 발생했습니다! ({e})")

    return


def view(schedules: list[Schedule], factor: str):
    if not schedules:
        print("기록된 일정이 존재하지 않습니다!")
        return

    if not factor:
        print_schedules(schedules)
    else:
        try:
            schedule_time = ScheduleTime(factor)
            search_period = schedule_time.to_period()

            found_schedules = [
                sch for sch in schedules if sch.period.overlaps(search_period)
            ]

            if not found_schedules:
                print("열람된 일정이 존재하지 않습니다!")
            else:
                print_schedules(found_schedules)

        except ValueError as e:
            print(f"오류: 열람 명령어의 인자인 일정시간을 다시 확인해 주십시오!")
            print("올바른 인자의 형태: 없거나 <일정시간>")
            # print(f"세부 오류: {e}")


def search(schedules: list[Schedule], factor: str):
    if not schedules:
        print("기록된 일정이 존재하지 않습니다!")
        return

    search_content = factor

    if not search_content:
        print_schedules(schedules)
    else:
        found_schedules = [
            sch for sch in schedules if search_content in sch.content.value
        ]

        if not found_schedules:
            print(f"검색된 일정이 존재하지 않습니다!")
        else:
            print_schedules(found_schedules)

def period(schedules: list[Schedule], factor: str):
    
    global id_num 

    if not factor:
        print("오류: 반복 명령어의 인자를 다시 확인해 주십시오!")
        print("올바른 인자의 형태: <일정번호> <공백열1> <반복유형> <공백열1> <반복횟수>")
        return

    try:
        parts = split_whitespace_1(factor, 1)
        
        if len(parts) != 2:
             print("오류: 반복 명령어의 인자를 다시 확인해 주십시오!")
             print("올바른 인자의 형태: <일정번호> <공백열1> <반복유형> <공백열1> <반복횟수>")
             return

        target_idx_str = parts[0]
        repeater_arg = parts[1]

        if not target_idx_str.isdigit():
            print("오류: 일정번호에 문자가 올 수 없습니다!")
            return
        
        target_idx = int(target_idx_str) - 1
        
        if target_idx < 0:
            print("오류: 일정번호에 양의 정수 값을 입력하세요!")
            return
        if target_idx >= len(schedules):
            print("오류: 입력한 번호에 해당하는 일정이 없습니다!")
            return
            
        target = schedules[target_idx]

        repeater = Repeater(target, repeater_arg)

        # [확인 1] 이미 반복 그룹에 속한 일정인지 확인
        current_repeat_id = 0
        if isinstance(target.repeat_id, int):
            current_repeat_id = target.repeat_id
        elif isinstance(target.repeat_id, str) and target.repeat_id.isdigit():
            current_repeat_id = int(target.repeat_id)
        if current_repeat_id > 0:
            print("오류: 반복 일정은 반복할 수 없습니다!")
            return

        # [확인 2] 반복 가능 여부 확인
        if not repeater.can_repeat():
            print("오류: 해당 일정의 기간은 반복 유형에서 불가능한 기간입니다!")
            return

        temp_schedules = repeater.get_repeat_schedules()
        if not temp_schedules:
            print("오류: 반복 일정을 생성하지 못했습니다!")
            return

        # [확인 3] 충돌 검사
        conflicts = []
        for temp_sch in temp_schedules:
            for existing_sch in schedules:
                if temp_sch.period.overlaps(existing_sch.period):
                    conflicts.append(existing_sch)
                    
        if conflicts:
            print("오류: 다음 일정과 기간이 충돌합니다!")
            conflict_sch = conflicts[0]
            print(f"{conflict_sch.number} {conflict_sch}")
            return

        # [모든 확인 통과 시]
        current_schedule_id = 0
        if isinstance(target.schedule_id, int):
            current_schedule_id = target.schedule_id
        elif isinstance(target.schedule_id, str) and target.schedule_id.isdigit():
            current_schedule_id = int(target.schedule_id)
        
        if current_schedule_id == 0:
            id_num += 1
            target.schedule_id = id_num
            
        target.repeat_id = target.schedule_id
        target.repeat_type = repeater.repeat_type
        target.repeat_count = repeater.repeat_count

        for new_sch in temp_schedules:
            id_num += 1
            new_sch.schedule_id = id_num
            new_sch.repeat_id = target.repeat_id
            new_sch.allow_overlap = target.allow_overlap
            
        schedules.extend(temp_schedules)
        save_schedules(schedules)
        
        print(f"일정이 다음과 같이 반복되었습니다!")
        
        display_list = [target] + temp_schedules
        print_schedules(display_list)

    except ValueError as e:
        if "Repeater" in str(e) or "repeat" in str(e):
             print(f"오류: 반복 설정이 잘못되었습니다! ({e})")
        elif "인자 개수" in str(e):
             print("오류: 반복 명령어의 인자 개수를 다시 확인해 주십시오!")
        else:
             print("오류: 잘못된 값이 입력되었습니다!")
    except Exception as e:
        print(f"오류: 반복 일정을 추가하는 중 문제가 발생했습니다! ({e})")

# endregion

# region 유틸리티 함수


def print_schedules(schedules: list[Schedule]):
    """일정 목록을 일정 번호와 함께 출력 (목업: '번호 일정내용')"""
    if not schedules:
        pass
    else:
        sort_schedule(schedules)
        for sch in schedules:
            print(f"{sch.number} {sch.allow_overlap} {sch}")


def print_command_list():
    """올바른 명령어 리스트 출력"""
    print("올바른 명령어를 입력해 주십시오!")
    print(
        "--------------------------------------------------------------------------------"
    )
    print("삭제 | 열람 | 검색 | 조정 | 변경 | 추가 | 종료")
    print(
        "--------------------------------------------------------------------------------"
    )
    print("ㅅㅈ | ㅇㄹ | ㄱㅅ | ㅈㅈ | ㅂㄱ | ㅊㄱ | ㅈㄹ")
    print(
        "--------------------------------------------------------------------------------"
    )
    print("delete | view | search | reschedule | change | add | quit")
    print(
        "--------------------------------------------------------------------------------"
    )
    print("d | v | s | r | c | a | q")
    print(
        "--------------------------------------------------------------------------------"
    )
    print("- | # | / | ! | @ | + | .")
    print(
        "--------------------------------------------------------------------------------"
    )


def sort_schedule(schedules: list[Schedule]):
    schedules.sort(
        key=lambda sch: (
            sch.period.start.to_datetime(),
            sch.period.end.to_datetime(),
            sch.schedule_id,
        )
    )


def update_schedule_number(schedules: list[Schedule]):
    for number, schedule in enumerate(schedules, start=1):
        schedule.number = number


# endregion


# region 메인 프롬프트
def main_prompt():
    is_valid = check_data_file()
    if not is_valid:
        return

    while True:
        # 일정이 수정되면 index 값이 변경되어야해서 while문 안으로 load_schedules함수를 넣었습니다.
        schedules = load_schedules()
        print_schedules(schedules)
        # region 반복자 테스트
        '''
        target = schedules[0]
        print("target")
        print(target)

        target.allow_overlap = False
        target.schedule_id = 15

        repeater = Repeater(target, "m 100")

        print("can repeat")
        print(repeater.can_repeat())

        print("get repeat schedules:")
        tmp = repeater.get_repeat_schedules()

        for tmp_schedule in tmp:
            print(
                f"{tmp_schedule}, {tmp_schedule.allow_overlap}, {tmp_schedule.repeat_id}"
            )
        '''
        # endregion

        prompt = input(">>> ")
        prompt = strip_whitespace_0(prompt)

        if not prompt:  # 명령어 없음
            print_command_list()
            continue

        parts = split_whitespace_1(prompt, 1)
        if len(parts) < 1:  # 명령어 없음
            print_command_list()
            continue

        # factor none 값 지정하여 if문에 오류가 안나게 했습니다.
        cmd = parts[0]
        # factor 변수 초기화
        """
        '>>> view'로 테스트한 결과
        해당 테스트처럼 part의 인덱스가 0밖에 없을 경우에도 factor를 사용해야 하는 경우가 존재합니다.
        하나, factor 변수가 if 내에서만 정의되어 위와 같은 상황에 에러가 발생하는 것을 확인했습니다.
        따라서 else를 추가하여 초기화하는 코드로 변경하였습니다.
        """
        factor = parts[1] if len(parts) == 2 else ""

        # 추가 기능
        if cmd in add_command_list:
            add(schedules, factor)

        # 삭제 기능
        elif cmd in delete_command_list:
            delete(schedules, factor)

        # 열람 기능
        elif cmd in view_command_list:
            view(schedules, factor)

        # 검색 기능
        elif cmd in search_command_list:
            search(schedules, factor)

        # 조정 기능
        elif cmd in reschedule_command_list:
            reschedule(schedules, factor)

        # 변경 기능
        elif cmd in change_command_list:
            change(schedules, factor)

        # 반복 기능
        elif cmd in period_command_list:
            period(schedules, factor)

        # 종료 기능
        elif cmd in quit_command_list:
            if not factor:
                break
            else:
                print("오류: 인자가 없어야 합니다!")

        else:
            print_command_list()
            continue


if __name__ == "__main__":
    main_prompt()
# endregion
