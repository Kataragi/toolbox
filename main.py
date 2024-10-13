import sys
import cv2
import os
from PIL import Image
import numpy as np
from tqdm import tqdm
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

x = 90
x_sense = 225
xbox_sense = 550
y = 90
y_sense = 0

class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ap1 = False  # 初期値を設定

        self.input_label = QtWidgets.QLabel(self)
        self.input_label.setText('処理する画像のあるフォルダー')
        self.input_label.move(x, y)

        self.input_line = QtWidgets.QLineEdit(self) # 
        self.input_line.move(x, y + 20)
        self.input_line.resize(500, 30)

        self.output_label = QtWidgets.QLabel(self)
        self.output_label.setText('保存するフォルダー')
        self.output_label.move(x, y * 2)

        self.output_line = QtWidgets.QLineEdit(self)
        self.output_line.move(x, y * 2 + 20)
        self.output_line.resize(500, 30)

        self.overlay_label = QtWidgets.QLabel(self)
        self.overlay_label.setText('オーバーレイする画像')
        self.overlay_label.move(x, y * 3)

        self.overlay_line = QtWidgets.QLineEdit(self)
        self.overlay_line.move(x, y * 3 + 20)
        self.overlay_line.resize(500, 30)

        self.mask_label = QtWidgets.QLabel(self)
        self.mask_label.setText('マスクする画像')
        self.mask_label.move(x, y * 4)

        self.mask_line = QtWidgets.QLineEdit(self)
        self.mask_line.move(x, y * 4 + 20)
        self.mask_line.resize(500, 30)

        self.extension_label = QtWidgets.QLabel(self)
        self.extension_label.setText('拡張子指定')
        self.extension_label.move(x + xbox_sense, y)

        self.extension_line = QtWidgets.QLineEdit(self) # 
        self.extension_line.move(x + xbox_sense, y + 20)
        self.extension_line.resize(500, 30)

        font = QtGui.QFont("游ゴシック", 12)
        self.input_line.setFont(font)
        self.output_line.setFont(font)
        self.overlay_line.setFont(font)
        self.mask_line.setFont(font)
        self.extension_line.setFont(font)
        

        self.button = QtWidgets.QPushButton('画像のモノクロ化', self)
        self.button.setFont(font)  # ボタンのフォントを設定
        self.button.move(x, y * 5)
        self.button.resize(200, 50)
        self.button.clicked.connect(self.monochrome_images)

        self.button = QtWidgets.QPushButton('画像の反転', self)
        self.button.setFont(font)  # ボタンのフォントを設定
        self.button.move(x + x_sense, y * 5)
        self.button.resize(200, 50)
        self.button.clicked.connect(self.inversion_images)

        self.button = QtWidgets.QPushButton('画像の二値化', self)
        self.button.setFont(font)  # ボタンのフォントを設定
        self.button.move(x + x_sense * 2, y * 5)
        self.button.resize(200, 50)
        self.button.clicked.connect(self.binarization_images)

        self.button = QtWidgets.QPushButton('画像のオーバーレイ', self)
        self.button.setFont(font)  # ボタンのフォントを設定
        self.button.move(x + x_sense * 3, y * 5)
        self.button.resize(200, 50)
        self.button.clicked.connect(self.overlay_images)

        self.button = QtWidgets.QPushButton('特定拡張子の削除', self)
        self.button.setFont(font)  # ボタンのフォントを設定
        self.button.move(x, y * 6)
        self.button.resize(200, 50)
        self.button.clicked.connect(self.overlay_images)

        self.button = QtWidgets.QPushButton('拡張子の統一', self)
        self.button.setFont(font)  # ボタンのフォントを設定
        self.button.move(x + x_sense * 1, y * 6)
        self.button.resize(200, 50)
        self.button.clicked.connect(self.unification_images)

        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.setGeometry(screen.width() // 2 - 140, screen.height() // 2, 1280, 780)
        self.move(320, 80)
        self.setWindowTitle('画像処理')

    def monochrome_images(self): # モノクロ化を処理する
        input_dir, output_dir = self.verify_directories()
        if input_dir is None or output_dir is None: # どちらかが None の場合、処理を停止
            return  # 早期リターンで処理を中止

        for image_name in tqdm(os.listdir(input_dir)): 
            image_path = os.path.join(input_dir, image_name)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            output_path = os.path.join(output_dir, image_name) # 保存パスの設定
            cv2.imwrite(output_path, image) # 画像の保存

    def inversion_images(self): # 画像の反転処理
        input_dir, output_dir = self.verify_directories()
        if input_dir is None or output_dir is None: # どちらかが None の場合、処理を停止
            return  # 早期リターンで処理を中止

        for image_name in tqdm(os.listdir(input_dir)):
            image_path = os.path.join(input_dir, image_name)
            image = cv2.imread(image_path)

            if image is not None:
                inverted_image = 255 - image
                output_path = os.path.join(output_dir, image_name) # 保存パスの設定
                cv2.imwrite(output_path, inverted_image) # 画像の保存

    def binarization_images(self): # 二値化処理
        input_dir, output_dir = self.verify_directories()
        if input_dir is None or output_dir is None: # どちらかが None の場合、処理を停止
            return  # 早期リターンで処理を中止

        for image_name in tqdm(os.listdir(input_dir)):
            image_path = os.path.join(input_dir, image_name)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # グレースケールで画像を読み込む

            if image is not None:
                _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
                output_path = os.path.join(output_dir, image_name) # 保存パスの設定
                cv2.imwrite(output_path, binary_image) # 画像の保存
            else:
                print(f"Failed to read {image_name}")

    def overlay_images(self, ap1): # 画像のオーバーレイ
        input_dir, output_dir, overlay_dir = self.verify2_directories()
        if input_dir is None or output_dir is None or overlay_dir is None: # どちらかが None の場合、処理を停止
            return  # 早期リターンで処理を中止

        for filename in tqdm(os.listdir(input_dir)):
            a_path = os.path.join(input_dir, filename)
            b_path = os.path.join(overlay_dir, filename)

            # Bフォルダーに同名のファイルが存在するか確認
            if os.path.isfile(b_path):
                # 画像を開く
                a_img = Image.open(a_path).convert("RGBA")
                b_img = Image.open(b_path).convert("RGBA")

                # オーバーレイ画像のサイズをAフォルダーの画像に合わせる
                b_img = b_img.resize(a_img.size)

                # 新しい画像を作成。元の画像をコピー
                combined_img = Image.new("RGBA", a_img.size)
                combined_img = Image.alpha_composite(combined_img, a_img)
                combined_img = Image.alpha_composite(combined_img, b_img)

                # 結果画像のパスを設定
                c_path = os.path.join(output_dir, filename)
                combined_img.save(c_path, format='PNG')  # 保存

    def unification_images(self): # 拡張子の統一
        input_dir, output_dir = self.verify_directories()

        allowed_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']  # 許可された拡張子のリスト
        extension = self.extension_line.text()  # 入力ディレクトリの検証
        extension = extension.lower()  # 指定された拡張子を正規化（小文字に統一）
        try:
            # 指定された拡張子が None の場合
            if extension is None or extension.lower() not in allowed_extensions:
                raise ValueError(f'許可された拡張子は {allowed_extensions} です')

        except (FileNotFoundError, ValueError) as e:
            QtWidgets.QMessageBox.critical(self, '警告', str(e))

        # 入力ディレクトリ内の全ファイルを処理
        for filename in tqdm(os.listdir(input_dir), desc="Processing images", unit="file"):
            # ファイルのフルパスを取得
            file_path = os.path.join(input_dir, filename)
            # 画像ファイルのみを処理
            if not os.path.isfile(file_path):
                continue
            # ファイル名と拡張子に分割
            base_name, ext = os.path.splitext(filename)
            # 拡張子が指定されたものと同じ場合、処理をスキップ
            if ext.lower() == extension:
                continue

            try:
                # 画像を開く
                img = Image.open(file_path)
                # CMYKモードの場合はRGBに変換
                if img.mode == 'CMYK':
                    img = img.convert('RGB')

                # 指定された拡張子に変換して保存
                new_filename = base_name + extension
                output_path = os.path.join(output_dir, new_filename)
                img.save(output_path)

            except Exception as e:
                print(f"Error processing {filename}: {e}")



    def verify_directories(self): # 入力フォルダーと出力フォルダーの検証
        try:
            input_dir = self.input_line.text()  # 入力ディレクトリの検証
            if not input_dir or not os.path.exists(input_dir):
                raise FileNotFoundError('入力ディレクトリが存在しません')

            # 出力ディレクトリの設定と検証
            output_dir = self.output_line.text() if self.output_line.text() else input_dir
            if not os.path.exists(output_dir):
                raise FileNotFoundError('出力ディレクトリが存在しません')

            if output_dir is None: #  outputフォルダーがNoneの場合、inputフォルダーと同じになるよう設定
                output_dir = input_dir

            return input_dir, output_dir  # 両方のディレクトリが問題ない場合はパスを返す

        except FileNotFoundError as e:
            QtWidgets.QMessageBox.warning(self, '警告', str(e))
            return None, None  # 問題があった場合はNoneを返す

    def verify2_directories(self): # 入力フォルダーと出力フォルダーの検証
        try:
            input_dir, output_dir = self.verify_directories()
            if input_dir is None or output_dir is None:
                raise FileNotFoundError('入力または出力ディレクトリに問題があります')

            overlay_dir = self.overlay_line.text()  # オーバーレイディレクトリの検証
            if not os.path.exists(overlay_dir):
                raise FileNotFoundError('オーバーレイディレクトリが存在しません')

            if output_dir is None: #  outputフォルダーがNoneの場合、inputフォルダーと同じになるよう設定
                output_dir = input_dir

            return input_dir, output_dir, overlay_dir  # 全てのディレクトリが問題ない場合はパスを返す

        except FileNotFoundError as e:
            QtWidgets.QMessageBox.warning(self, '警告', str(e))
            return None, None, None  # 問題があった場合はNoneを返す

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()