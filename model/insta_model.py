
class InstaPost:
    datetime_int = 0
    caption = ""
    urls = []

    def __str__(self):
        result = str(self.datetime_int) + '\n'
        result += self.caption + '\n'
        for i in self.urls:
            result += i + '\n'
        return result