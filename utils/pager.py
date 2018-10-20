class PageInfo1(object):

    def __init__(self,current_page,all_count,per_page,base_url,show_page=5):
        #current_page:当前页  all_count:数据总个数, per_page：每页显示多少条数据   base_url:url地址   show_page:页面显示几条页码
        try:
            self.current_page = int(current_page)   #当前页强制转换整数,防止是字符串输入
        except Exception as e:
            self.current_page = 1        #当前页可能不是数字，出现异常转第一页
        self.per_page = per_page         #每页显示多少条数据

        a,b = divmod(all_count,per_page)  #总数据个数除以每页显示条数,a是除数结果，b是余数
        if b:   #判断余数
            a = a + 1
        self.all_page = a     #all_page  总页码
        self.show_page = show_page   #页面显示11条页码
        self.base_url = base_url

    def start(self):
        return  (self.current_page-1) * self.per_page     #起始位置

    def end(self):
        return self.current_page * self.per_page           #结束位置

    def pager(self):                                      #显示页码
        page_list = []
        half = int((self.show_page-1)/2)        # half等于5个
        #如果数据库总页数 < 11
        if self.all_page < self.show_page:     #如果总页数 < 数据库显示的页数
            begin = 1
            stop = self.all_page + 1
        # 总页数 > 11
        else:
            #如果当前页 <= 5，一直显示1到11页
            if self.current_page <= half:
                begin = 1
                stop = self.show_page + 1
            # 如果当前页 > 5，显示页码往后移
            else:
                #判断最后截至页,
                if self.current_page + half > self.all_page:
                    begin = self.all_page - self.show_page + 1   #总页数-显示页数+1，静态显示起始页
                    stop = self.all_page + 1
                #如果不到最后截至页
                else:
                    begin = self.current_page - half
                    stop = self.current_page + half + 1
        #上一页
        if self.current_page <= 1:     #如果当前页<=1
            prev = "<li><a href='/shebei/?page=#/'>上一页</a></li>"
        else:
            prev = "<li><a href='%s?page=%s'>上一页</a></li>" %(self.base_url,self.current_page-1,)  #当前页 - 1
        page_list.append(prev)

        for i in range(begin,stop):               #页码范围
            if i == self.current_page:                    #判断是否为当前页，如果为当前页设置背景色
                temp = "<li class='active'><a href='%s?page=%s'>%s</a></li>" %(self.base_url,i,i,)   #生成每一个a标签，可以在这加入样式
            else:
                temp = "<li><a href='%s?page=%s'>%s</a></li>" % (self.base_url,i, i,)
            page_list.append(temp)

        # 下一页
        if self.current_page >= self.all_page:  # 如果当前页>=总页数
            nex = "<li><a href='/shebei/?page=*/'>下一页</a></li>"
        else:
            nex = "<li><a href='%s?page=%s'>下一页</a></li>" %(self.base_url,self.current_page + 1,)  # 当前页 + 1
        page_list.append(nex)

        return ''.join(page_list)          #将所有页码拼接起来