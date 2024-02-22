from requests_html import HTMLSession


def main(id):
    r = HTMLSession()
    data = {
        'IRN': id,
        'Name & Address': '',
        'Notification Date': '',
        'Status': '',
        'Link': ''
    }
    name = ''
    holder_name = ''
    date = ''
    link = ''
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB, en',
        'q': '0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': '',
        'Host': 'www3.wipo.int',
        'Pragma': 'no-cache',
        'Referer': 'https://www3.wipo.int/madrid/monitor/en/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    }
    url = f"https://www3.wipo.int/madrid/monitor/jsp/getData.jsp?qi=1-jnvFk5iv20G7hx4h4BDUdRRFkKJkMgISgqrYGXtmwwM=&ID=ROM.{str(id)}&LANG=en&NO=0&TOT=1"
    try:

        html = r.get(url, headers=headers)
        html = html.html

        # Finding Name and Address

        divs = html.find('div.p')
        for div in divs:

            if div.text.find('Name and address of the representative') != -1:
                name = '\n'.join(div.text.split('\n')[2:])
                break

            if div.text.find('Name and address of the holder of the registration') != -1:
                holder_name = '\n'.join(div.text.split('\n')[2:])
        if name == '':
            name = holder_name

        # Finding Notification Date and Links:

        divs = html.find('div.description.box_content.retreci')
        found  = False
        for div in divs:
            # print(div.text)
            if div.text.find('IN') != -1 and div.text.find('580') != -1:
                # print(div.text)
                text = div.text.split('\n')
                try:
                    index = text.index('Date of notification')
                except:
                    continue
                date = text[index+1]
                link = list(div.links)[0]
                found = True
                continue
            elif (not found) and div.text.find('PH') != -1 and div.text.find('580') != -1:
                    # print(div.text)
                    text = div.text.split('\n')
                    try:
                        index = text.index('Date of notification')
                    except:
                        continue
                    date = text[index+1]
                    link = list(div.links)[0]
                    continue
                
        data = {
            'IRN': id,
            'Name & Address': name,
            'Notification Date': date,
            'Status': '',
            'Link': link
        }
    except Exception as e:
        print(e)

    # print(data)
    return data


if __name__ == '__main__':
    print(main(1611367))
