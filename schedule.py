import os
import re
import sys
from datetime import date
from datetime import datetime


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
        return f"{self.value:02d}시"


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
        return f"{self.value:02d}분"


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
    new_schedule = Schedule(factor)
    for idx, sch in enumerate(schedules):
        if new_schedule.period.overlaps(sch.period):
            print("오류: 다음 일정과 기간이 겹칩니다!")
            print("-> ", idx + 1, sch)
            break
    else:
        schedules.append(new_schedule)
        print("일정이 추가되었습니다!")
        save_schedules(schedules)
    return schedules


def reschedule(schedules, factor) -> list[Schedule]:
    try:
        r_factors = split_whitespace_1(factor, 1)
        idx = int(r_factors[0]) - 1

        if idx < 0:
            print("오류: 일정번호에 양의 정수 값을 입력하세요!")
            return schedules
        if idx >= len(schedules):
            print("오류: 입력한 일정번호에 해당하는 일정이 없습니다!")
            return schedules

        r_sch = r_factors[1]
        schedule = schedules[idx]
        comsch = Schedule(r_sch)

        for idx, sch in enumerate(schedules):
            if comsch.period.overlaps(sch.period):
                print("오류: 다음 일정과 기간이 겹칩니다!")
                print("-> ", idx + 1, sch)
                break
        else:
            schedule.period = comsch.period
            save_schedules(schedules)
            print("일정이 다음과 같이 조정되었습니다!")
            print(
                "(주의: 일정 순서의 변동으로 인해 해당 일정의 번호가 변경되었습니다!)"
            )
            schedules = load_schedules()
            for idx2, sch in enumerate(schedules):
                if sch.period.start.to_datetime() == comsch.period.start.to_datetime():
                    print(idx2 + 1, sch)
                    break
        return schedules

    except ValueError:
        try:
            float_val = float(idx)
            print("오류: 일정번호에 양의 정수 값을 입력하세요!")
        except:
            print("오류: 일정번호에 문자가 올 수 없습니다!")
        return schedules


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
            continue

        parts = split_whitespace_1(prompt, 1)
        if len(parts) < 1:  # 명령어 없음
            continue

        # factor none 값 지정하여 if문에 오류가 안나게 했습니다.
        cmd = parts[0]
        factor = parts[1] if len(parts) == 2 else ""

        if len(parts) == 2:
            factor = parts[1]

        if cmd in add_command_list:
            if not factor:
                print("오류: 추가 명령어의 인자인 일정을 다시 확인해 주십시오!")
                print("올바른 인자의 형태: <기간> <공백열1> <일정내용>")
                continue
            schedules = add(schedules, factor)
        elif cmd in view_command_list:
            if not schedules:
                print("등록된 일정이 없습니다.")
            else:
                for i, sch in enumerate(schedules, start=1):
                    print(f"{i}: {sch}")
        elif cmd in reschedule_command_list:
            if not factor:
                print("오류: 조정 명령어의 인자를 다시 확인해 주십시오!")
                print("올바른 인자의 형태: <일정번호> <공백열1> <기간>")
                continue
            schedules = reschedule(schedules, factor)
        elif cmd in change_command_list:
            if not factor:
                print("오류: 변경 명령어의 인자를 다시 확인해 주십시오!")
                print(
                    "올바른 인자의 형태: <일정번호> 혹은 <일정번호> <공백열1> <일정내용>"
                )
                continue
            schedules = change(schedules, factor)
        elif cmd in quit_command_list:
            print("프로그램을 종료합니다.")
            break

        else:
            print("올바른 명령어를 입력하세요.")


if __name__ == "__main__":
    main_prompt()
# endregion
