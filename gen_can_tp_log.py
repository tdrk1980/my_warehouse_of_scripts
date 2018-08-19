# *-* encoding: utf-8 *-*
import argparse

# 定数
dlc       = 8
header="""date Thu Aug 9 11:55:27.680 am 2018
base hex  timestamps absolute
internal events logged
// version 9.0.0
Begin Triggerblock Thu Aug 9 11:55:27.680 am 2018"""


def get_can_log(timestamp,ch,dlc,data):
    '''
    CANログフォーマットの文字列にするユーティリティ関数
    '''
    return f"{timestamp:>11.6f} {ch:<2} {can_id:3X}             Tx   d {dlc:1} {data}"


def print_tp_frame(timestamp, ch, can_id, user_data, t_wait_FC=0.1, t_wait_CF=0.01):
    '''
    データ(data)をCAN TP形式に分割する関数
    '''

    # データ長(data_len)によって処理を振り分け
    user_data_len = len(user_data)
    if 0 <= user_data_len <= 7:
        # Single Frameのヘッダ
        SF = f"0{user_data_len:1X}"

        # 与えられた数値の配列(list)を文字列に変換して、間をスペースで埋めて結合。7バイトに満たない場合は、"00"に埋める
        DATA = " ".join([f"{i:02X}" for i in user_data] + ["00"] * (7-user_data_len))

        # SFとDATAを足してcan_frameにする
        can_frame = SF + " " + DATA

        # SFの出力-
        print(get_can_log(timestamp, ch, dlc, can_frame))

    elif 7 < user_data_len <= 4095:

        # First Frame(FF)のヘッダ
        FF = f"1{(user_data_len&0xF00)>>8:1X} {user_data_len&0xFF:02X}"

        DATA = " ".join([f"{i:02X}" for i in user_data[:6]])

        # FFとDATAを足してcan_frameにする
        can_frame = FF + " " + DATA

        # FFの出力
        print(get_can_log(timestamp, ch, dlc, can_frame))

        # CFのデータを抽出
        cf_data = user_data[6:]

        # ConsecutiveFrame(CF)数を計算する
        # CF数 = CF長 ÷ 7 + 0 ・・・CF長が7で割り切れる
        #                 + 1  ・・・CF長が7で割り切れない
        CF_num = len(cf_data) // 7
        CF_num += 0 if len(cf_data) % 7 == 0 else 1

        # Flow Control(FC)を待つ時間を加える
        timestamp += t_wait_FC

        # CFの処理
        for i in range(1, CF_num+1): # CFのSequence Numberは 21から始まるのでi=1から始める(終了が1つずれるのでCF_num+1とする)
            # CFのヘッダ
            CF = f"2{i % 0x10:1X}"

            # 7個ずつ切り出し。7個に満たない場合は、0を付け足す
            can_data = cf_data[7*(i-1)+0:7*(i-1)+7]
            can_data += [0]*(7-len(can_data))

            DATA = " ".join([f"{i:02X}" for i in can_data])

            can_frame = CF + " " + DATA

            # CFを出力
            print(get_can_log(timestamp, ch, dlc, can_frame))

            # 次のCF向けのwaitを入れる
            timestamp += t_wait_CF
    else:
        print(f"データ長が0～4095の範囲内に入っていない。len(user_data) = {user_data_len} ")


def gen_tp_log(timestamp,ch,dlc,data):
    print(header)
    print_tp_frame(timestamp,ch,dlc,data)

if __name__ == "__main__":  
    # 適宜設定
    timestamp = 0.277523
    ch        = 1
    can_id    = 0x7fe

    # TPの連結したデータをイメージした文字列
    s = "11220304050607"

    # 2文字づつ分割
    slist = [s[i: i+2] for i in range(0, len(s), 2)]

    # 数値の配列(list)に変換 ・・・16進数でない文字列が入っているケースを止めるためにやる
    data = [int(s,16) for s in slist]

    gen_tp_log(timestamp, ch, can_id, data)
