from twocaptcha import TwoCaptcha


class Solver:
    # TODO use class for error handling of twocaptcha system, and raise adequate errors or deal with errors locally
    def __init__(self, api_key: str) -> None:
        self.solver = TwoCaptcha(api_key)

    # so far only used for refactoring
    def solve(self, img_path: str) -> str:
        result = self.solver.normal(img_path)
        return result["code"]
