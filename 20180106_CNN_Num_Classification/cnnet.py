# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
import random as rd
import load_output_data as ld

#卷积核中权重及偏置
def weight_bias_init(shape_w,shape_b,name_w,name_b):
    init_w=tf.truncated_normal(shape=shape_w,stddev=0.01)
    init_b=tf.constant(0.1,shape=shape_b)
    return [tf.Variable(init_w,name=name_w),tf.Variable(init_b,name_b)]


#卷积操作
def conv2d(x,w):
    temp=tf.nn.conv2d(x,w,[1,1,1,1],'SAME')
    return temp


#池化操作
def pool_max_2x2(x):
    temp=tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
    return temp


def create_batch(min_queue,b_size,X_train,y_lable):
    cap=2*b_size+min_queue
    [train_set,lable]=tf.train.shuffle_batch([X_train,y_lable],batch_size=b_size,
                                            capacity=cap,min_after_dequeue=min_queue)
    return [train_set,lable]
    


def ccnet():
    tf.reset_default_graph()
    
    #读入数据
    print('正在读取数据......')
    [X_train,label]=ld.load_train_data('train_data.csv')
    print('读取数据完毕！')
    print('-----------------------------------------')
    
    #定义占位符
    X=tf.placeholder('float',[None,784],name='X')
    y_label=tf.placeholder('float',[None,10],name='y_lable')
    keep_prob=tf.placeholder(tf.float32,name='keep_prob')
    #[X_batch_train,y_batch_label]=create_batch(min_queue=1000,b_size=500,X_train=X_train,y_lable=lable)
    
    #参数初始化
    [wc1,bc1]=weight_bias_init([5,5,1,32],[32],'wc1','bc1')
    [wc2,bc2]=weight_bias_init([5,5,32,64],[64],'wc2','bc2')
    [wfc1,bfc1]=weight_bias_init([7*7*64,1024],[1024],'wfc1','bfc1')
    [wfc2,bfc2]=weight_bias_init([1024,10],[10],'wfc2','bfc2')
    
    #定义第一层卷积层
    x_image=tf.reshape(X,[-1,28,28,1])
    h_conv1=tf.nn.relu(conv2d(x_image,wc1)+bc1)
    h_pool1=pool_max_2x2(h_conv1)
    
    #定义第二层卷积层
    h_conv2=tf.nn.relu(conv2d(h_pool1,wc2)+bc2)
    h_pool2=pool_max_2x2(h_conv2)
    
    #定义第一层全连接层
    h_flat=tf.reshape(h_pool2,[-1,7*7*64])
    h_fc1=tf.nn.relu(tf.matmul(h_flat,wfc1)+bfc1)
    
    #Dropout层
    h_fc1_drop=tf.nn.dropout(h_fc1,keep_prob)
    
    #输出层
    y=tf.nn.softmax(tf.matmul(h_fc1_drop,wfc2)+bfc2)
    
    cross_entropy=-tf.reduce_sum(y_label*tf.log(y),reduction_indices=[1]) #交叉熵
    train_step=tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)  #Adam优化算法
    
    sess=tf.InteractiveSession()
    sess.run(tf.global_variables_initializer())
    
    saver=tf.train.Saver()
    tf.add_to_collection('predict',y)
    tf.add_to_collection('train_step',train_step)
    
    print('开始训练......')
    for k in range(1000):
        i=rd.randint(0,41499)
        sess.run(train_step,feed_dict={X:X_train[i:i+500],y_label:label[i:i+500],keep_prob:0.5})
        if(k%100==0):
            print('已经进行了'+str(int(k/100))+'百次训练')
        
    print('训练完毕！')
    print('------------------------------------------')
    
    print('正在保持模型.......')
    saver.save(sess,'graph_saver/old/model_test.ckpt')
    print('模型保存完毕！')
    print('******************************************')


def ccnet_train_warmstart():
    tf.reset_default_graph()
    
    #读入数据
    print('正在读取数据......')
    [X_train,label]=ld.load_train_data('train_data.csv')
    print('读取数据完毕！')
    print('-----------------------------------------')
    
    #进入会话
    with tf.Session() as sess:
        #导入模型及操作
        new_saver=tf.train.import_meta_graph('graph_saver/new/model_test_new.ckpt.meta')
        new_saver.restore(sess,'graph_saver/new/model_test_new.ckpt')
        train_step=tf.get_collection('train_step')[0]
        
        graph=tf.get_default_graph()
        
        #获取占位符
        X=graph.get_operation_by_name('X').outputs[0]
        y_lable=graph.get_operation_by_name('y_lable').outputs[0]
        keep_prob=graph.get_operation_by_name('keep_prob').outputs[0]
        
        saver=tf.train.Saver()
    
        print('在上次结果的基础上再次训练2000次.....')
        for k in range(2000):
            i=rd.randint(0,41499)
            sess.run(train_step,feed_dict={X:X_train[i:i+500],y_lable:label[i:i+500],keep_prob:0.5})
            if(k%100==0):
                print('已经进行了'+str(int(k/100))+'百次训练')
                
        print('训练完成！')
        print('---------------------------------------------')
        
        print('正在保存最近训练得到的模型')
        saver.save(sess,'graph_saver/new/model_test_new.ckpt')
        print('模型保存完毕！')
        print('*********************************************')


def ccnet_predict():
    result=np.array(np.zeros(28000))
    
    print('读入测试集数据')
    X_test=ld.load_test_data('test_data.csv')
    print('读入完成')
    print('-------------------------------')
    with tf.Session() as sess:
        new_saver=tf.train.import_meta_graph('graph_saver/old/model_test.ckpt.meta')
        new_saver.restore(sess,'graph_saver/old/model_test.ckpt')
        y=tf.get_collection('predict')[0]
        
        graph=tf.get_default_graph()
        
        X=graph.get_operation_by_name('X').outputs[0]
        keep_prob=graph.get_operation_by_name('keep_prob').outputs[0]
        
        print('正在预测测试集数据......')
        for k in range(28):
            result[1000*k:1000*(k+1)]=sess.run(tf.argmax(y,1),feed_dict={X:X_test[1000*k:1000*(k+1)],keep_prob:1.0})
        
        ld.output_result(result,'ccnet_result.csv')
        print('已输出预测结果')
        print('*************************************')
        
        return(result)
        
               
if __name__=='__main__':
    ccnet()   
    ccnet_predict()