
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


BILLS = {
    0: '第7案：你是否同意以「平均每年至少降低1%」之方式逐年降低火力發電廠發電量？',
    2: '第8案：您是否同意確立「停止新建、擴建任何燃煤發電廠或發電機組（包括深澳電廠擴建）」之能源政策？',
    4: '第9案：你是否同意政府維持禁止開放日本福島311核災相關地區，包括福島與周遭4縣市（茨城、櫪木、群馬、千葉）等地區農產品及食品進口？',
    6: '第10案：你是否同意民法婚姻規定應限定在一男一女的結合?',
    8: '第11案：你是否同意在國民教育階段內（國中及國小），教育部及各級學校不應對學生實施性別平等教育法施行細則所定之同志教育？',
    10: '第12案：你是否同意以民法婚姻規定以外之其他形式來保障同性別二人經營永久共同生活的權益？',
    12: '第13案：你是否同意，以「台灣」（Taiwan）為全名申請參加所有國際運動賽事及2020年東京奧運？',
    14: '第14案：您是否同意，以民法婚姻章保障同性別二人建立婚姻關係？',
    16: '第15案：您是否同意，以「性別平等教育法」明定在國民教育各階段內實施性別平等教育，且內容應涵蓋情感教育、性教育、同志教育等課程？',
    18: '第16案：您是否同意：廢除電業法第95條第1項，即廢除「核能發電設備應於中華民國一百十四年以前，全部停止運轉」之條文？'
}


class CommandLine:

    def get_source(self):
        URL = 'http://referendum.2018.nat.gov.tw/pc/zh_TW/00/00000000000000000.html'
        response = requests.get(URL).text
        bs = BeautifulSoup(response, features='lxml')
        results = []
        for x in bs.select('tr.trT'):
            results.append([y for y in x.text.split('\n') if y])
        return results

    def restruct(self):
        results = self.get_source()
        counter = 0
        data = dict()
        cases = dict()
        for line in results:
            if counter % 2 == 0:
                cases[int(counter / 2)] = dict(
                    bill=BILLS.get(counter),
                    assent=int(line[0].replace(',', '')),
                    dissent=int(line[1].replace(',', '')),
                    valid=int(line[2].replace(',', '')),
                    invalid=int(line[3].replace(',', ''))
                )

            if counter % 2 == 1:
                cases[int((counter - 1) / 2)].update(dict(
                    total_votes=int(line[0].replace(',', '')),
                    eligible_voter=int(line[1].replace(',', '')),
                    vote_rate=float(line[2].replace('%', '')),
                    rate=float(line[3].replace('%', ''))
                ))
            counter += 1
        return cases

    def outcome(self):
        cases = self.restruct()
        cate = ['nuclear', 'nuclear', 'nuclear', 'sexual', 'sexual', 'sexual', 'naming', 'sexual', 'sexual', 'nuclear']
        lines = []
        for key, case in self.restruct().items():
            category = cate[key]
            diff = case['assent'] - case['dissent']
            rate_pass = bool(case['rate'] > 25.0)
            is_pass = bool(diff > 0 and rate_pass)

            if rate_pass:
                is_rate_pass = COLOR.OKGREEN + str(rate_pass).title() + COLOR.ENDC
            else:
                is_rate_pass = COLOR.FAIL + str(rate_pass).title() + COLOR.ENDC

            if is_pass:
                is_pass_color = COLOR.OKGREEN + str(is_pass).title() + COLOR.ENDC
            else:
                is_pass_color = COLOR.FAIL + str(is_pass).title() + COLOR.ENDC

            data = dict(
                category=category,
                case_no=int(key+7),
                bill=case['bill'],
                assent=case['assent'],
                dissent=case['dissent'],
                rate=case['rate'],
                rate_pass=is_rate_pass,
                is_pass=is_pass_color,
                diff=diff
            )
            lines.append(data)
        return lines

    def output(self):
        while True:
            print(datetime.now().strftime('%H:%M'))
            for line in self.outcome():
                print(line['bill'])
                print(
                    'Category: {category} | Case No.: {case_no} | Assent:Dissent {assent}:{dissent} | Rate: {rate}| Rate Pass: {rate_pass} | Is Pass: {is_pass} | Diff: {diff} '.format_map(line))
                print('\n')
            time.sleep(30)


if __name__ == "__main__":
    Fire(CommandLine)
