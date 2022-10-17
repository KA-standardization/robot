from django.db import models


# Create your models here.

class RobotNun(models.Model):
    class Meta:
        db_table = 'robot_num'

    number = models.IntegerField()
    state = models.CharField(max_length=32)

    def to_dict(self):
        return {'number': self.number, 'state': self.state, 'id': self.id}


class Actions(models.Model):
    action = models.CharField(max_length=32)
    time_set = models.DateTimeField()

    # 	on_delete=None,               # 删除关联表中的数据时,当前表与其关联的field的行为
    # 	on_delete=models.CASCADE,     # 删除关联数据,与之关联也删除
    # 	on_delete=models.DO_NOTHING,  # 删除关联数据,什么也不做
    # 	on_delete=models.PROTECT,     # 删除关联数据,引发错误ProtectedError
    # 	# models.ForeignKey('关联表', on_delete=models.SET_NULL, blank=True, null=True)
    # 	on_delete=models.SET_NULL,    # 删除关联数据,与之关联的值设置为null（前提FK字段需要设置为可空,一对一同理）
    # 	# models.ForeignKey('关联表', on_delete=models.SET_DEFAULT, default='默认值')
    # 	on_delete=models.SET_DEFAULT, # 删除关联数据,与之关联的值设置为默认值（前提FK字段需要设置默认值,一对一同理）
    # 	on_delete=models.SET,         # 删除关联数据,
    # 	 a. 与之关联的值设置为指定值,设置：models.SET(值)
    # 	 b. 与之关联的值设置为可执行对象的返回值,设置：models.SET(可执行对象)
    r_num = models.ForeignKey(RobotNun, on_delete=models.CASCADE)

    def to_dict(self):
        return {'action': self.action, 'time_set': self.time_set, 'r_num': self.r_num}
