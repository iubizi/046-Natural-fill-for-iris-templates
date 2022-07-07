import cv2
import numpy as np

def process(input_path, output_path, file_name):

    # 可能出现的路径错误
    # try，有可能是空的路径
    try:
        if input_path[-1] != '/': input_path += '/'
    except: pass 
    try:
        if output_path[-1] != '/': output_path += '/'
    except: pass

    # 读取 虹膜 模板 瞳孔 需要平滑的区域
    iris = cv2.imread( input_path + file_name )
    
    # print(iris)
    if iris is None: return # 非图片结束
    
    # 调整大小到 268 268
    iris = cv2.resize(iris, (268,268), interpolation=cv2.INTER_CUBIC)
    
    template = cv2.imread('template.png', cv2.IMREAD_UNCHANGED) # channel=4
    pupil = cv2.imread('pupil.png', cv2.IMREAD_UNCHANGED)
    iris_mask = cv2.imread('iris_mask.png')

    # 虹膜替换透明区域
    # iris: x=261, y=357, r=134, sz=268
    index = np.where(template[:,:,3]<127)
    template[index[0],index[1],:3] = \
                                   iris[index[0]-261+134,index[1]-357+134,:]

    # 瞳孔替换中心圆
    # pupil: x=261-45, y=357-45, r=45, sz=90
    index = np.where(pupil[:,:,3]>127)
    template[index[0]+261-45,index[1]+357-45,:] = \
                                                pupil[index[0],index[1],:]

    template = template[:,:,:3]

    def blur(edge_size, blur_size): # blur_size must be odd number
        # 边缘和膨胀
        edge = cv2.Canny(iris_mask[:,:,0], 10, 70)

        kernel = np.ones( (edge_size, edge_size), dtype='uint8' )  
        edge = cv2.dilate(edge, kernel, iterations=1)

        # 分开处理，去除高频信号
        r = cv2.GaussianBlur(template[:,:,0], (blur_size, blur_size), 0)
        g = cv2.GaussianBlur(template[:,:,1], (blur_size, blur_size), 0)
        b = cv2.GaussianBlur(template[:,:,2], (blur_size, blur_size), 0)

        # 替换原始像素
        index = np.where(edge>127)
        template[index[0],index[1],0] = r[index[0],index[1]]
        template[index[0],index[1],1] = g[index[0],index[1]]
        template[index[0],index[1],2] = b[index[0],index[1]]

    blur(edge_size=10, blur_size=5)
    blur(edge_size=7, blur_size=7)
    blur(edge_size=5, blur_size=9)
    blur(edge_size=3, blur_size=13)

    print('imwrite', output_path + file_name) # 提示一下
    cv2.imwrite( output_path + file_name, template )

if __name__ == '__main__':

    # process('', 'out', '119_3.png')
    pass
    '''
    # 不用代码仓库
    cv2.imshow('imshow', template)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
