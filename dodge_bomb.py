import os
from random import randint
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = {  #移動用辞書
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, 5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(5, 0),  #カンマを書く癖があるといい
}
trandDeta ={  #移動座標に対応する角度のデータ 
    (0, 0):0,   #初期データ（推していないときの処理用）
    (-5, 0):0,  #←
    (-5, -5):315,   #左上
    (0, -5):270,   #↑
    (5, -5):225,   #右上
    (5, 0):180,  #→
    (5, 5):135,  #左下
    (0, 5):90,   #↓
    (-5, 5):45,   #左下
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def init_bom_imgs() -> tuple[list[pg.Surface], list[int]]:
    boms = []
    for r in range(1, 11):
        bom = pg.Surface((20*r, 20*r))  #画面大きさの定義
        pg.draw.circle(bom, (255, 0, 0), (10*r, 10*r), 10*r)  #円大きさの定義
        bom.set_colorkey((0, 0, 0))  #透過度
        boms.append(bom)
    accs = [a for a in range(1, 11)]  #加速度
    return boms, accs
        

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    clock = pg.time.Clock()
    tmr = 0
    trans = 0 #こうかとんの向きの調整変数[tate, yoko]
    boms, accs = init_bom_imgs()  #爆弾等の初期化設定
    bom = boms[0]  #爆弾の処理設定
    bom_rct = bom.get_rect()  #bomのrect
    bom_rct.center = randint(10, WIDTH-10), randint(10, HEIGHT-10)
    vx, vy = +5, +5  # 爆弾の横方向速度，縦方向速度
    avx, avy = 0, 0 # 爆弾の横方向加速度，縦方向加速度
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bom_rct):  #衝突判定
            game_over(screen)  #gameover判定
            return "game over"
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if trans != trandDeta[(sum_mv[0], sum_mv[1])]:
            if (sum_mv[0], sum_mv[1]) != (0, 0): #向いているときの箇所が違うときの設定
                trans = trandDeta[(sum_mv[0], sum_mv[1])]  #初期化を無視する判定
                kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)  #角度の初期化
                if trans >90  and trans <= 270:  #反対を向く際の反転判定
                    #反対向くための処理
                    kk_img = pg.transform.flip(kk_img, False, True)
                kk_img = pg.transform.rotozoom(kk_img, trans, 1.0)  #回転処理
        if check_bound(kk_rct)  != (True, True):  #跳ね返り処理
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        screen.blit(bom, bom_rct)
        pg.display.update()
        tmr += 1
        bom_rct.move_ip(vx + avx, vy +avy)
        yoko, tate = check_bound(bom_rct)
        if not yoko:  #横の跳ねかえり
            vx *= -1
        if not tate :  #縦跳ね返り
            vy *= -1
        bom = boms[min(tmr//500, 9)]  #爆弾の大きさ処理
        avx = vx*accs[min(tmr//500, 9)]  #
        avy = vy*accs[min(tmr//500, 9)]
        clock.tick(50) 
 

def bom_change()->tuple:
    boms = []
    for r in range(1, 11): 
        bom = pg.Surface((20*r, 20*r)) 
        pg.draw.circle(bom, (255, 0, 0), (10*r, 10*r), 10*r)
        boms.append((bom, pg.draw.circle(bom, (255, 0, 0), (10*r, 10*r), 10*r)))
    return tuple(boms)


def check_bound(obj_rct:pg.Rect)-> tuple[bool, bool]: 
    """
    引数:こうかとんRect爆弾Rect
    戻り値:タプル（横判定結果、縦判定結果）
    画面内ならTRUE、画面外ならFALSE
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:  #横判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom :  #縦判定
        tate = False
    return yoko, tate


def game_over(screen)-> None:
    sq = pg.Surface((WIDTH, HEIGHT))
    pg.draw.circle(sq, (255, 255, 255), (0, 0), 0)
    sq.set_alpha(50)
    end_img = pg.image.load("fig/8.png")  #画像のロード
    end_rct1 = end_img.get_rect()  #rect定義
    end_rct1.center = WIDTH/2+500, HEIGHT/2  #配置場所
    end_rct2 = end_img.get_rect()
    end_rct2.center = WIDTH/2-500, HEIGHT/2
    screen.blit(sq, [0, 0])
    fonto = pg.font.Font(None, 120) 
    txt = fonto.render("game over", True, (255, 255, 255)) 
    screen.blit(txt, [WIDTH/2-250, HEIGHT/2])
    screen.blit(end_img, end_rct1)
    screen.blit(end_img, end_rct2)
    pg.display.update()  #画面の更新
    pg.time.wait(5000)  #5秒間表示


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
