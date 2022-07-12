# ANPR_ocr

本篇旨在利用 python 撰寫出一套可行的車牌辨識系統 , 並能夠在 arm ( aarch64-linux ) 架構的開發板( embedded linux )上進行辨識,
並提供即時的串流影像於螢幕上<br/>

## 要準備的套件( 皆為 pythhon )
  1. opencv3 ( 才有 opencv_createsamples.exe )
  2. numpy
  3. imutils

## 使用技術

> 影像處理( 訓練資料的準備 ):

   1. labelimg<br/>
   2. [ch-tseng大大製作的 negatives 以及 positives 文件產生器](https://github.com/ch-tseng/cascade_opencv_train)<br/>
    
> 機器學習:

   1. opencv_createsamples.exe ( opencv4 已經移除 )<br/>
   2. opencv_traincascade.exe  ( opencv4 已經移除 )<br/>

> 影像輸出:

   FrameBuffer<br/>
   
## 實作方法

我先透過 LBP 分類器將車牌及車子分離出來 , 再取最大矩形面積 , 希望能夠藉此避免框選到其他與車牌無關的東西 ,<br/>
最後再送給 ocr 做辨識, 不過樣本僅有 58 張 , 加上我不太清楚台灣車牌的字體到底是什麼( 僅知道這是澳洲字體 ),<br/>
訓練 ocr 時只能餵 微軟正黑體 給他學, 也許未來知道字體跟有足夠的樣本後之後可以再做個 CNN 版本的ocr

