
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from fire import Fire


class COLOR:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class CommandLine:

    def get_progress(self):
        URL = 'http://vote.2018.nat.gov.tw/pc/zh_TW/TC/sm63000000000000000.html'
        response = requests.get(URL).text
        bs = BeautifulSoup(response, features='lxml')
        results = []
        return bs.select('tr.trFooterT')[0].text[-11:]

    def get_source(self):
        URL = 'http://vote.2018.nat.gov.tw/pc/zh_TW/TC/sm63000000000000000.html'
        response = requests.get(URL).text
        bs = BeautifulSoup(response, features='lxml')
        results = []
        for x in bs.select('tr.trT'):
            results.append([y for y in x.text.split('\n') if y])
        voting = dict()

        for person in results:
            voting.update({int(person[1]): dict(
                number=int(person[1]),
                name=person[2],
                votes=int(person[4].replace(',', '')),
                rate=float(person[5].replace('%', '')))
            })
        return voting.get(4), voting.get(2)

    def outcome(self):
        while True:
            kp, ding = self.get_source()
            vote_diff = int(kp['votes'] - ding['votes'])
            if vote_diff > 0:
                dominator = COLOR.OKGREEN + kp['name'] + COLOR.ENDC
            else:
                dominator = COLOR.FAIL + ding['name'] + COLOR.ENDC

            print(datetime.now().strftime('%H:%M'))
            print('{kp_name}:{ding_name} \nVoting: {kp_vote}:{ding_vote} \nRate: {kp_rate}:{ding_rate} \nVote Diff: {vote_diff} \nRate Diff: {rate_diff} \nDominator: {dominator} \nProgress: {progress}'.format(
                kp_name=kp['name'],
                ding_name=ding['name'],
                kp_vote=kp['votes'],
                ding_vote=ding['votes'],
                kp_rate=kp['rate'],
                ding_rate=ding['rate'],
                vote_diff=int(kp['votes'] - ding['votes']),
                rate_diff="%.2f" % round(float(kp['rate'] - ding['rate']), 2),
                dominator=dominator,
                progress=self.get_progress()
            ))
            print('\n\n')
            time.sleep(30)


if __name__ == "__main__":
    Fire(CommandLine)
