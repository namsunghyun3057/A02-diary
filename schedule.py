import os
import re
import sys
from datetime import date
from datetime import datetime
from calendar import monthrange


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
        self.value = self._parse(strip_whitespace_0(s))

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
        self.value = self._parse(strip_whitespace_0(s))

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
        self.value = self._parse(strip_whitespace_0(s))

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
        s_stripped = strip_whitespace_0(s)
        self.year, self.month, self.day = self._parse(s_stripped)
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
        self.value = self._parse(strip_whitespace_0(s))

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
        self.value = self._parse(strip_whitespace_0(s))

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
        self.hour, self.minute = self._parse(strip_whitespace_0(s))
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
        self.date, self.time = self._parse(strip_whitespace_0(s))

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
        self.start, self.end = self._parse(strip_whitespace_0(s))

    def _parse(self, s):
        start, end = s.split("~", 1)

        start_dt = DateTime(start)
        end_dt = DateTime(end)

        if start_dt.to_datetime() > end_dt.to_datetime():
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
        self.period, self.content = self._parse(strip_whitespace_0(s))

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

    def __str__(self):
        if len(self.content.value) == 0:
            return f"{self.period}"
        else:
            return f"{self.period} {self.content}"


# class 일정시간 추가해야 합니다
class ScheduleTime:
    """
    일정시간. <년>, <년/월>, <날짜> 형식을 파싱하고 Period로 변환
    """

    def __init__(self, s: str):
        self._parse(strip_whitespace_0(s))

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


# endregion


# region 데이터 파일
DATA_FILE = "schedule_data.txt"


def check_data_file():
    """데이터 파일 존재 확인 및 생성"""
    if not os.path.exists(DATA_FILE):
        print("데이터 파일이 없습니다. 새로 생성합니다...")
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                pass
        except PermissionError:
            print(
                "오류: 현 경로에 데이터 파일 생성을 실패했습니다. 프로그램을 종료합니다."
            )
            sys.exit(1)
    else:
        print("데이터 파일이 확인되었습니다.")

    if not os.access(DATA_FILE, os.R_OK | os.W_OK):
        print(f"{os.path.abspath(DATA_FILE)}")
        print("에 대한 입출력 권한이 없습니다. 프로그램을 종료합니다.")
        sys.exit(1)


def load_schedules() -> list[Schedule]:
    """파일에서 일정 목록 불러오기"""
    schedules = []
    if not os.path.exists(DATA_FILE):
        return schedules
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n\r")
            if line:
                try:
                    parts = line.split("\t")

                    if len(parts) != 11:
                        raise ValueError(
                            "데이터 파일이 형식에 맞지 않습니다. (line: {line})"
                        )

                    schedule = (
                        "/".join(parts[0:3])
                        + " "
                        + ":".join(parts[3:5])
                        + "~"
                        + "/".join(parts[5:8])
                        + " "
                        + ":".join(parts[8:10])
                        + " "
                        + parts[10]
                    )

                    schedules.append(Schedule(schedule))
                except Exception as e:
                    print(f"[데이터 오류] {e}")
    schedules.sort(key=lambda sch: sch.period.start.to_datetime())
    return schedules


def save_schedules(schedules: list[Schedule]):
    """일정 목록을 파일에 저장"""
    schedules = sorted(schedules, key=lambda sch: sch.period.start.to_datetime())

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for sch in schedules:
            start = sch.period.start
            end = sch.period.end
            content = sch.content.value

            line = (
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
# endregion

# region 명령어 함수


def add(schedules, factor) -> list[Schedule]:
    try:
        new_schedule = Schedule(factor)
    except ValueError:
        print("오류: 추가 명령어의 인자인 일정을 다시 확인해 주십시오!")
        print("올바른 인자의 형태: <추가> <공백열1> <일정>")
        return schedules

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
    return schedules


def reschedule(schedules, factor) -> list[Schedule]:
    try:
        r_factors = split_whitespace_1(factor, 1)
        check = 1
        idx = int(r_factors[0]) - 1
        print(idx)
        check = 0
        if idx < 0:
            print("오류: 일정번호에 양의 정수 값을 입력하세요!")
            return schedules
        if idx >= len(schedules):
            print("오류: 입력한 일정번호에 해당하는 일정이 없습니다!")
            return schedules
        if len(r_factors) < 2:
            print("오류: 조정 명령어의 인자를 다시 확인해 주십시오!")
            print("올바른 인자의 형태: <일정번호> <공백열1> <기간>")
            return schedules

        r_sch = r_factors[1]
        schedule = schedules[idx]
        comsch = Schedule(r_sch)
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
            schedules = load_schedules()

            if idx < len(schedules):
                same_order = (
                    schedules[idx].period.start.to_datetime()
                    == comsch.period.start.to_datetime()
                    and schedules[idx].period.end.to_datetime()
                    == comsch.period.end.to_datetime()
                )
            else:
                same_order = False

            if not same_order:
                print(
                    "(주의: 일정 순서의 변동으로 인해 해당 일정의 번호가 변경되었습니다!)"
                )
            for idx2, sch in enumerate(schedules):
                if sch.period.start.to_datetime() == comsch.period.start.to_datetime():
                    print(idx2 + 1, sch)
                    break
            return schedules

    except ValueError:
        try:
            if check:
                float_val = float(r_factors[0])
                print("오류: 일정번호에 양의 정수 값을 입력하세요!")
            else:
                print("오류: 조정 명령어의 인자를 다시 확인해 주십시오!")
                print("올바른 인자의 형태: <일정번호> <공백열1> <기간>")
        except:
            print("오류: 일정번호에 문자가 올 수 없습니다!")
        return schedules
    except IndexError:
        print("오류: 조정 명령어의 인자를 다시 확인해 주십시오!")
        print("올바른 인자의 형태: <일정번호> <공백열1> <기간>")
        return schedule


def change(schedules, factor):
    try:
        c_factors = split_whitespace_1(factor, 1)
        idx = int(c_factors[0]) - 1
        content = None

        if idx < 0:
            print("오류: 일정번호에 양의 정수 값을 입력하세요!")
            return schedules
        if idx >= len(schedules):
            print("오류: 입력한 일정번호에 해당하는 일정이 없습니다!")
            return schedules
        if len(c_factors) == 2:
            content = c_factors[1]
        if not content:
            content = ""
        schedules[idx].content = Content(content)
        save_schedules(schedules)
        return schedules
    except ValueError:
        try:
            float_val = float(idx)
            print("오류: 일정번호에 양의 정수 값을 입력하세요!")
        except:
            print("오류: 일정번호에 문자가 올 수 없습니다!")
        return schedules


def delete(schedules: list[Schedule], factor: str) -> list[Schedule]:
    if not schedules:
        print("기록된 일정이 없어 삭제할 수 없습니다!")
        return schedules
    try:
        delete_index = int(factor)

        if 1 <= delete_index <= len(schedules):
            schedule_to_delete = schedules[delete_index - 1]

            print(
                f"[{delete_index} {schedule_to_delete}]을(를) 정말로 삭제하시겠습니까? (Y/N) "
            )
            confirm = input(">>> ")
            confirm = confirm.strip(" \t\f\v").upper()

            if confirm == "Y":
                schedules.pop(delete_index - 1)
                print(
                    f"일정 [{delete_index} {schedule_to_delete}]이(가) 삭제되었습니다."
                )
                save_schedules(schedules)
            else:
                print("삭제를 취소합니다.")
        else:
            print(
                f"오류: 일정 번호가 유효한 범위(1 ~ {len(schedules)})를 벗어났습니다!"
            )

    except ValueError:
        print("오류: 일정 번호는 숫자여야 합니다!")
    except Exception as e:
        print(f"오류: 일정을 삭제하는 중 문제가 발생했습니다! ({e})")

    return schedules


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
            found_schedules = []
            for sch in schedules:
                if sch.period.overlaps(search_period):
                    found_schedules.append(sch)
            if not found_schedules:
                print(f" '{schedule_time}'에 겹치는 일정이 없습니다!")
            else:
                print_schedules(found_schedules)

        except ValueError as e:
            print(f"오류: 열람 명령어의 인자인 일정시간을 다시 확인해 주십시오!")
            print("올바른 인자의 형태: <열람> 또는 <열람> <공백열1> <일정시간>")
            print(f"세부 오류: {e}")


def search(schedules: list[Schedule], factor: str):
    if not schedules:
        print("기록된 일정이 존재하지 않습니다!")
        return

    search_content = factor

    if not search_content:
        print_schedules(schedules)
    else:
        found_schedules = []
        for sch in schedules:
            if search_content in sch.content.value:
                found_schedules.append(sch)

        if not found_schedules:
            print(f"일정 내용에 '{search_content}'을(를) 포함하는 일정이 없습니다!")
        else:
            print_schedules(found_schedules)


# endregion


# region 유틸리티 함수


def print_schedules(schedules: list[Schedule]):
    """일정 목록을 일정 번호와 함께 출력"""
    if not schedules:
        print("등록된 일정이 없습니다.")
    else:
        # 출력 전, 일정을 시작 시각 순으로 다시 정렬 (명령어 로직에 따라 순서가 꼬일 수 있으므로)
        schedules.sort(key=lambda sch: sch.period.start.to_datetime())
        for i, sch in enumerate(schedules, start=1):
            # 일정 출력 형식에 맞게 출력: "일정번호: 일정내용"
            # Schedule.__str__에서 이미 기간을 포함한 형식으로 출력됨
            print(f"{i} {sch}")


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


# endregion


# region 메인 프롬프트
def main_prompt():
    check_data_file()

    while True:
        # 일정이 수정되면 index 값이 변경되어야해서 while문 안으로 load_schedules함수를 넣었습니다.
        schedules = load_schedules()
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
            if not factor:
                print("오류: 추가 명령어의 인자인 일정을 다시 확인해 주십시오!")
                print("올바른 인자의 형태: <기간> <공백열1> <일정내용>")
                continue

            try:
                schedules = add(schedules, factor)

            except ValueError as e:
                print(f"오류: 일정 형식에 문제가 있습니다! ({e})")
            except Exception as e:
                print(f"오류: 일정을 추가하는 중 문제가 발생했습니다! ({e})")

        # 삭제 기능
        elif cmd in delete_command_list:
            if not factor:
                print("오류: 삭제 명령어의 인자인 일정번호를 다시 확인해 주십시오!")
                print("올바른 인자의 형태: <삭제> <공백열1> <일정번호>")
                continue
            schedules = delete(schedules, factor)

        # 열람 기능
        elif cmd in view_command_list:
            view(schedules, factor)

        # 검색 기능
        elif cmd in search_command_list:
            search(schedules, factor)

        # 조정 기능
        elif cmd in reschedule_command_list:
            if not factor:
                print("오류: 조정 명령어의 인자를 다시 확인해 주십시오!")
                print("올바른 인자의 형태: <일정번호> <공백열1> <기간>")
                continue
            schedules = reschedule(schedules, factor)

        # 변경 기능
        elif cmd in change_command_list:
            if not factor:
                print("오류: 변경 명령어의 인자를 다시 확인해 주십시오!")
                print(
                    "올바른 인자의 형태: <일정번호> 혹은 <일정번호> <공백열1> <일정내용>"
                )
                continue
            schedules = change(schedules, factor)

        # 종료 기능
        elif cmd in quit_command_list:
            if not factor:
                print("프로그램을 종료합니다.")
                break
            else:
                print("오류: 인자가 없어야 합니다!")

        else:
            print_command_list()
            continue


if __name__ == "__main__":
    main_prompt()
# endregion
