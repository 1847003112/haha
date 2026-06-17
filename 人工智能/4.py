import numpy as np
# list_1d =[1,2,3,4,5]
# arr_1d = np.array(list_1d)
# list_2d=[[1,2,3],[4,5,6],[7,8,9]]
# arr_2d=np.array(list_2d)
# list_3d=[[[1,2],[3,4]],[[5,6],[7,8]]]
# arr_3d=np.array(list_3d)
# print(arr_1d)
# print(arr_2d)
# print(arr_3d)
# print('维度:',arr_2d.ndim)
# print('形状:',arr_1d.shape)
# print('元素总数:',arr_2d.size)
# print('元素类型:',arr_2d.dtype)
# n=np.random.rand(2,3)
# print(n)
# m=np.linspace(0,6,5)
# print(m)
# y=np.arange(0,11,5)
# print(y)
# print(np.eye(3))
# print(np.ones((3,3)))
# print(np.full((2,2),7))
# arr=np.arange(12)
# print(arr.reshape(3,4))
# print(arr.reshape(2,-1))
# arr = np.array([[1, 2, 3], [4, 5, 6]])
# print(arr.T) 
# arr1=np.array([[1,2],[3,4]])
# arr2=np.array([[5,6],[7,8]])
# print(np.concatenate((arr1,arr2),0))
# print(np.concatenate((arr,arr2),1))

# scores = np.random.randint(0, 101, size=(2, 5, 3))
# print("成绩（班级,学生,科目）:\n", scores)
#  class_avg = scores.mean(axis=(1, 2))
# print("\n每个班级的平均成绩:", class_avg)
# objoct_avg=scores.mean(axis=1)
# print('\n每个班级每门课的平均成绩:',objoct_avg)
# n = np.median(scores, axis=(0, 1))
# print("\n每门课的中位数:", n)
# student_max = scores.max(axis=2)
# student_min = scores.min(axis=2)
# print("\n每个学生的最高分:\n", student_max)
# print("每个学生的最低分:\n", student_min)
# print(scores[0,:,:])
# print(scores[:,2,:])
# print(scores[1,3:,:2])
# print(scores[:,:,-1])
# grades = np.array([[[77, 66, 88],[99, 78, 91],[55, 65, 89]],[[33, 44, 55],[66, 77, 88],[99, 88, 87]]])
# mask = grades >= 90
# print(mask)
# high_grades = grades[mask]
# print(high_grades)
# adj_grades=np.where(grades<60,60,grades)
# print(adj_grades)
# grades1=grades[0,:,:]
# mask=grades1>=85
# high_grades1=grades1[mask]
# print(high_grades1)
# n=np.where(grades >= 90, '优秀',np.where(grades >= 60, '合格', '不合格'))
# print(n)
# m =np.any(grades < 60,axis=2)
# x = grades[m]       
# print(x)
a=np.array([[[1,2,3],[3,4,5]],[[4,5,6],[4,5,5]]])
b=np.array([[[2,3,2],[2,3,5]],[[1,2,3],[5,5,6]]])
c=np.array([[[1,1,1],[2,2,2]],[[3,3,3],[2,2,2]]])
m=a+b
print(m)
n=a-b
print(n)
x=a*b
print(x)

