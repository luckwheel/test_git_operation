import cv2
import os
import random
import matplotlib.pyplot as plt

def drew_box():
    import cv2
import numpy as np

import cv2
import numpy as np

from functools import cmp_to_key

from functools import cmp_to_key

def sort_points_by_position(list_of_points):
    if not list_of_points:
        return []
    
    # 计算每个多边形的外接矩形（x_min左, y_min上, x_max右, y_max下）
    rect_info = []
    for idx, points in enumerate(list_of_points):
        int_points = [[round(float(x)), round(float(y))] for x, y in points]
        x_coords = [p[0] for p in int_points]
        y_coords = [p[1] for p in int_points]
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        rect_info.append((x_min, y_min, x_max, y_max, idx))
    
    def compare(rect_a, rect_b):
        x_min_a, y_min_a, x_max_a, y_max_a, _ = rect_a
        x_min_b, y_min_b, x_max_b, y_max_b, _ = rect_b
        
        # 情况1：a完全在b的上方（a的底部 ≤ b的顶部）→ a优先（上→下）
        if y_max_a <= y_min_b:
            return -1  # a在b前
        # 情况2：b完全在a的上方（b的底部 ≤ a的顶部）→ b优先（上→下）
        if y_max_b <= y_min_a:
            return 1   # b在a前
        # 情况3：垂直重叠（同一水平面）→ 严格按左→右排序（左边界小的优先）
        if x_min_a < x_min_b:
            return -1  # a在左，a优先
        else:
            return 1   # b在左，b优先
    
    # 应用自定义比较函数排序
    sorted_rects = sorted(rect_info, key=cmp_to_key(compare))
    sorted_points = [list_of_points[idx] for (_, _, _, _, idx) in sorted_rects]
    
    return sorted_points

def draw_multiple_bboxes_on_image(image_path, list_of_points, output_path=None, 
                                 colors=None, thickness=2, fill=False, sort=True):
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"错误: 无法读取图片 {image_path}")
        return

    if not list_of_points:
        print("错误: 坐标列表为空")
        return
    
    # 按位置排序（如果需要）
    if sort:
        list_of_points = sort_points_by_position(list_of_points)
    
    # 生成颜色列表
    if colors is None:
        np.random.seed(42)  # 固定随机种子，确保结果可重现
        colors = [tuple(np.random.randint(0, 256, 3).tolist()) for _ in range(len(list_of_points))]
    
    # 绘制每个边界框
    for i, points in enumerate(list_of_points):
        # 转换浮点数坐标为整数
        int_points = [
            [round(float(x)), round(float(y))]
            for [x, y] in points
        ]
        
        points_array = np.array(int_points, dtype=np.int32).reshape((-1, 1, 2))
        color = colors[i % len(colors)]
        
        if fill:
            cv2.fillPoly(image, [points_array], color=color)
        else:
            # 绘制多边形边框
            cv2.polylines(image, [points_array], isClosed=True, color=color, thickness=thickness)
            
            # 在每个顶点上画点
            for (x, y) in int_points:
                cv2.circle(image, (x, y), 3, (0, 0, 255), -1)  # 红色实心点
        
        # 在边界框旁边添加编号（按排序后的顺序）
        if len(list_of_points) > 1:
            x, y = int_points[0]
            cv2.putText(image, f"#{i+1}", (x, y-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    # 保存结果或显示图片
    if output_path:
        cv2.imwrite(output_path, image)
        print(f"已保存图片到 {output_path}")
    else:
        # 使用matplotlib显示（转换为RGB格式）
        plt.figure(figsize=(10, 10))
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title("带边界框的图片")
        plt.axis('off')
        plt.show()
    
    return image


def get_true_extension(filename, valid_extensions=('.jpg', '.jpeg', '.png', '.txt')):
    """
    智能提取文件名的真实扩展名，处理多重后缀的情况
    """
    text = sorted(valid_extensions, key=len, reverse=True)
    print(text)
    for ext in sorted(valid_extensions, key=len, reverse=True):
        if filename.lower().endswith(ext):
            return ext
    return os.path.splitext(filename)[1]  # 默认回退到标准方法

def rename_file_name(img_path,txt_path):
        img_file_list = [img_name.rsplit('.', 1)[0] for img_name in os.listdir(img_path)]
        txt_file_list = [txt_name.rsplit('.', 1)[0] for txt_name in os.listdir(txt_path)]
        
        common_file_name_list = list(set(img_file_list) & set(txt_file_list))
        for index, old_name in enumerate(common_file_name_list, start=1): 
            # 统一文件名
            new_base_name = f"{index:08d}"
            
            # 重命名图片文件（保留原始后缀）
            for img_file in os.listdir(img_path):
                img_base, img_ext = os.path.splitext(img_file)
                if img_base == old_name:
                    old_img_path = os.path.join(img_path, img_file)
                    new_img_name = f"{new_base_name}.jpg"
                    new_img_path = os.path.join(img_path, new_img_name)
                    os.rename(old_img_path, new_img_path)
                    print(f"图片文件重命名: {img_file} -> {new_img_name}")
            
            # 重命名文本文件（使用.txt后缀）
            for txt_file in os.listdir(txt_path):
                txt_base, txt_ext = os.path.splitext(txt_file)
                if txt_base == old_name:
                    old_txt_path = os.path.join(txt_path, txt_file)
                    new_txt_name = f"{new_base_name}.txt"
                    new_txt_path = os.path.join(txt_path, new_txt_name)
                    os.rename(old_txt_path, new_txt_path)
                    print(f"文本文件重命名: {txt_file} -> {new_txt_name}")
                

        
if __name__ == '__main__':
    img_path = r'F:\test_drew_fix_coord\images'
    txt_path = r'F:\test_drew_fix_coord\txt'
    output_path = r'F:\test_drew_fix_coord\label_imgs'
        # 现有图片路径
    image_path = "path_to_your_image.jpg"
    
    # 定义多个四边形的坐标（示例数据）
    list_of_points = []
    
    # 为每个框指定颜色（BGR格式）
    custom_colors = [
        (0, 0, 255),    # 红色
        (0, 255, 0),    # 绿色
        (255, 0, 0)     # 蓝色
    ]
    
    # # 在图片上绘制多个边界框并显示
    # draw_multiple_bboxes_on_image(
    #     image_path=image_path,
    #     list_of_points=list_of_points,
    #     colors=custom_colors,
    #     thickness=3
    # )
    for i in range(1, 101):
        # 格式化文件名，确保正确补零
        img_test_path = os.path.join(img_path, f'00000{i:03d}.jpg')
        txt_test_path = os.path.join(txt_path, f'00000{i:03d}.txt')
        
        # 检查文件是否存在
        if not os.path.exists(img_test_path):
            print(f"图片不存在: {img_test_path}")
            continue
        if not os.path.exists(txt_test_path):
            print(f"txt文件不存在: {txt_test_path}")
            continue
        
        print(f"处理文件: {txt_test_path}")
        
        # 读取坐标
        coords = []
        try:
            with open(txt_test_path, 'r', encoding='utf-8') as f:
                for line in f:
                    coord = line.strip().split(',')[0:8]  # 提取坐标并去除首尾空白
                    if len(coord) == 8:  # 确保有完整的4个坐标点
                        coords.append(coord)
        except Exception as e:
            print(f"读取文件失败: {txt_test_path}, 错误: {e}")
            continue
        
        if not coords:
            print(f"文件中没有有效坐标: {txt_test_path}")
            continue
        
        # 每次处理新图片前重置列表
        list_of_points = []
        
        # 转换坐标格式
        for coord in coords:
            # 将每8个值拆分为4个坐标点 [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
            points = [coord[i:i+2] for i in range(0, len(coord), 2)]
            list_of_points.append(points)
        
        # 指定输出路径，避免覆盖原图
        output_path = os.path.join(output_path, f'00000{i:03d}_bbox.jpg')
        #传入的数据
        '''
        [[['34.38', '21.25'], ['34.38', '96.25'], ['719.38', '96.25'], ['719.38', '21.25']], [['26.88', '121.25'], ['26.88', '150.0'], ['78.13', '150.0'], ['78.13', '121.25']], [['80.63', '113.75'], ['80.63', '151.25'], ['666.88', '151.25'], ['666.88', '113.75']], [['35.63', '166.25'], ['35.63', '202.5'], ['169.38', '202.5'], ['169.38', '166.25']], [['639.38', '230.0'], ['639.38', '263.75'], ['709.38', '263.75'], ['709.38', '230.0']], [['85.63', '566.25'], ['84.38', '597.5'], ['151.88', '597.5'], ['151.88', '566.25']], [['181.7', '334.09'], ['196.02', '302.73'], ['205.57', '301.36'], ['186.48', '337.5']], [['182.39', '347.73'], ['182.39', '342.27'], ['188.52', '342.27'], ['188.52', '347.73']], [['187.16', '338.86'], ['212.39', '291.82'], ['219.2', '291.82'], ['192.61', '341.59']], [['189.89', '345.68'], ['193.98', '349.77'], ['225.34', '293.18'], ['220.57', '292.5']], [['196.7', '349.77'], ['226.7', '292.5'], ['233.52', '295.91'], ['201.48', '351.14']], [['208.98', '340.91'], ['232.84', '294.55'], ['238.98', '297.27'], ['217.16', '341.59']], [['506.95', '439.69'], ['506.95', '483.75'], ['513.98', '483.75'], ['513.98', '439.69']], [['497.58', '423.75'], ['497.58', '432.19'], ['505.08', '432.19'], ['505.08', '423.75']], [['498.05', '437.34'], ['498.05', '452.34'], ['502.73', '452.34'], ['502.73', '437.34']], [['497.11', '461.25'], ['497.11', '469.22'], ['501.8', '469.22'], ['501.8', '461.25']], [['495.23', '469.69'], ['495.23', '487.5'], ['501.8', '487.5'], ['501.8', '469.69']], [['488.2', '422.81'], ['488.2', '444.38'], ['494.77', '444.38'], ['494.77', '422.81']], [['488.2', '447.19'], ['485.86', '488.44'], ['492.89', '488.91'], ['492.89', '447.19']], [['477.42', '423.28'], ['477.42', '495.0'], ['481.64', '495.0'], ['481.64', '423.28']], [['465.7', '431.72'], ['465.7', '487.5'], ['473.67', '487.5'], ['473.67', '431.72']], [['433.83', '591.09'], ['431.02', '557.34'], ['558.05', '560.63'], ['558.52', '593.44']], [['53.52', '722.73'], ['71.25', '686.59'], ['693.07', '685.23'], ['689.66', '722.05']]]
        '''
        # print(list_of_points)
        # 绘制并保存结果
        draw_multiple_bboxes_on_image(
            image_path=img_test_path,
            list_of_points=list_of_points,
            output_path=output_path,
            colors=None,
            thickness=3
        )
