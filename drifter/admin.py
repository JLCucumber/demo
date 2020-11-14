from django.contrib import admin
from drifter.models import *


class StatusFilter(admin.SimpleListFilter):
    title = "性别"
    parameter_name = "sex"

    def lookups(self, request, model_admin):
        return (
            ('0','男'),
            ('1','女'),
        )
    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(sex="0")
        elif self.value() == '1':
            return  queryset.filter(sex="1")

@admin.register(drifter_user)
class Registers(admin.ModelAdmin):
    list_display = ["nicheng","username","password","sex"]
    search_fields = ("nicheng","username")
    #选中条目个数显示
    actions_selection_counter = True
    #action功能摆放位置

    #过滤器
    list_filter = (StatusFilter,)

    #允许只读字段
    list_filter = (StatusFilter,)

    #按时间过滤
    #date_hierarchy = 'create_time'

    #每页显示条数
    #list_display_links = [25]

    #自定义动作列表
    actions = ['status_0','status_1']

    def status_0(self,request,queryset):
        row_updated = queryset.update(nicheng='caixukun')
        self.message_user(request,"修改了{}条字段".format(row_updated))
    status_0.short_description = '昵称修改'

    def status_1(self,request,queryset):
        row_updated = queryset.update()

        #

# Register your models here.
