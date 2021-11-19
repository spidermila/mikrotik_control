from typing import Any
from typing import Dict
from typing import List


def cprint(rows) -> None:  # type: ignore
    column_widths: Dict[int, Any] = {}
    for row in rows:
        for number, column in enumerate(row):
            current_column_width = len(str(column))
            if number not in column_widths.keys():
                column_widths[number] = current_column_width
            else:
                if column_widths[number] <= current_column_width:
                    column_widths[number] = current_column_width

    output: List[str] = []
    for row in rows:
        new_row = ''
        for number, column in enumerate(row):
            new_row += f'{column:<{column_widths[number]}}'
        output.append(new_row)

    for item in output:
        print(item)
