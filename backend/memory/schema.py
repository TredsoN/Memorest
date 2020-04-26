import graphene
from django.db import transaction
from graphene_django import DjangoObjectType
from graphene import ObjectType, String, Schema
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from memory.models import Memory, Subject
from user.models import User


class MemoryType(DjangoObjectType):
    class Meta:
        model = Memory


class SubjectType(DjangoObjectType):
    class Meta:
        model = Subject


class MemoryQuery(graphene.ObjectType):
    all_memory = graphene.List(MemoryType)
    all_subject = graphene.List(SubjectType)

    def resolve_all_memory(self, info, **kwargs):
        return Memory.objects.all()

    def resolve_all_subject(self, info, **kwargs):
        return Subject.objects.all()


class MemoryInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    creatorUsername = graphene.String(required=True)
    picture = graphene.String(required=True)
    audio = graphene.String(required=True)
    content = graphene.String(required=True)
    privacy = graphene.Int(required=True)
    subjectId = graphene.Int()
    subjectName = graphene.String()


class CreateMemory(Output, graphene.Mutation):
    """
    创建记忆

    访问条件： \n
    用户已登录 (请求中需要携带JWT token)

    参数: \n
    title!: 记忆标题 \n
    creatorUsername!: 创建人用户名（留空表示为当前已登录用户） \n
    picture!: 图片文件地址 \n
    audio!: 音频文件地址 \n
    content!: 记忆内容 \n
    privacy!: 私密/公开记忆(0/1) \n
    subjectId: 记忆主题id，此两项只需选填一个即可，都不填则不使用记忆主题\n
    subjectName: 记忆主题名称，此两项只需选填一个即可，都不填则不使用记忆主题\n

    返回值: \n
    success: 操作是否成功 \n

    示例：\n
    mutation {
        createMemory(memoryData:{title:"memory1", creatorUsername:"李在学", picture:"",audio:"",content:"this is one memory", privacy:1, subjectId:3}){
        success
      	errors
        }
    }
    """

    class Arguments:
        memory_data = MemoryInput(required=True)

    @login_required
    def mutate(self, info, memory_data):
        with transaction.atomic():
            user = info.context.user
            memory = Memory.objects.create()
            memory.title = memory_data['title']
            if memory_data['creatorUsername'] == "":
                memory.creatorId = user.id
                memory.creatorUsername = user.username
            else:
                memory.creatorId = User.objects.get(username=memory_data['creatorUsername']).id
                memory.creatorUsername = memory_data['creatorUsername']
            if memory_data['subjectId']:
                if Subject.objects.filter(id=memory_data['subjectId']).exists():
                    memory.subjectId=memory_data['subjectId']
                    memory.subjectName=Subject.objects.get(id=memory_data['subjectId']).name
                else:
                    return CreateMemory(success=False, errors={"subjectId": "该subject不存在"})
            elif memory_data['subjectName']:
                if Subject.objects.filter(name=memory_data['subjectName']).exists():
                    memory.subjectId=Subject.objects.get(id=memory_data['subjectName']).id
                    memory.subjectName=memory_data['subjectName']
                else:
                    return CreateMemory(success=False, errors={"subjectName": "该subject不存在"})
            memory.picture = memory_data['picture']
            memory.audio = memory_data['audio']
            memory.content = memory_data['content']
            memory.privacy = memory_data['privacy']
            memory.save()
            return CreateMemory(success=True)


class DeleteMemory(graphene.Mutation):
    """
    删除记忆

    参数: \n
    id!: 记忆id \n

    返回值: \n
    success: 操作是否成功 \n

    示例：\n
    mutation {
        deleteMemory( memoryId:5){
        success
        }
    }
    """
    success = graphene.Boolean()

    class Arguments:
        memoryId = graphene.Int(required=True)

    def mutate(self, info, memoryId):
        with transaction.atomic():
            memory = Memory.objects.get(id=memoryId)
            Subject.objects.get(id=memory.subjectId).delete()
            memory.delete()
            return DeleteMemory(success=True)


class SearchMemory(graphene.Mutation):
    """
    搜索记忆

    参数: \n
    keyword!: 关键字 \n

    返回值: \n
    success: 操作是否成功 \n

    示例：\n
    mutation {
        searchMemory( keyword:'memory'){
        subjects{
          id,
          name,
          createTime
        },
        success
        }
    }
    """
    success = graphene.Boolean()
    subjects = graphene.List(SubjectType)

    class Arguments:
        keyword = graphene.String(required=True)

    def mutate(self, info, keyword):
        subjects = Subject.objects.filter(name__icontains=keyword)
        return SearchMemory(subjects=subjects, success=True)


class GetAllMemory(graphene.Mutation):
    """
    获取所有记忆

    参数: \n
    creatorUsername: 用户用户名(不填则表示获取所有用户的所有记忆) \n
    aliveOnly： 仅获取存活的记忆(默认为True) \n

    返回值: \n
    memorys： 该用户创建的所有的记忆 \n
    success: 操作是否成功 \n

    示例：\n
    mutation{
      getAllMemory(){
        memorys{
          id,
          title,
          picture,
          audio,
          content,
          createTime,
          privacy,
          subjectId,
          subjectName
        },
        success
      }
    }
    """
    success = graphene.Boolean()
    memorys = graphene.List(MemoryType)

    class Arguments:
        creatorUsername = graphene.String()
        aliveOnly = graphene.Boolean()

    def mutate(self, info, creatorUsername='', aliveOnly=True):
        if creatorUsername == '':
            memorys = Memory.objects.all()
        else:
            memorys = Memory.objects.filter(creatorUsername=creatorUsername)
        if aliveOnly:
            memorys = memorys.exclude(activity=0)
        return GetAllMemory(memorys=memorys, success=True)


class ReadOneMemory(graphene.Mutation):
    """
    查看某条记忆

    参数: \n
    memoryId!: 记忆编号 \n
    isOwner!: 查看者是否为记忆主人(True/False) \n

    返回值: \n
    memory： 该条记忆的信息 \n
    success: 操作是否成功 \n

    示例：\n
    mutation{
      readOneMemory(memoryId:3, isOwner:true){
        memory{
          id,
          title,
          picture,
          audio,
          content,
          createTime,
          privacy,
          subjectId,
          subjectName
        },
        success
      }
    }
    """
    success = graphene.Boolean()
    memory = graphene.Field(MemoryType)

    class Arguments:
        memoryId = graphene.Int(required=True)
        isOwner = graphene.Boolean(required=True)

    def mutate(self, info, memoryId, isOwner):
        memory = Memory.objects.get(id=memoryId)
        if isOwner and memory.deathtime==0:
            memory.recallTime +=1
            memory.activity = 100# + memory.recallTime * 100
            # memory.deathtime = 0
        else:
            memory.visitor += 1
        memory.save()
        return ReadOneMemory(memory=memory, success=True)


class GetRandomDeadMemory(graphene.Mutation):
    """
    随机获取一批死去记忆

    参数: \n
    number: 获取数量(默认15条) \n
    creatorUsername: 创建者用户名(不填表示从所有用户的死去的公开记忆中获取) \n

    返回值: \n
    memorys： 获取到的记忆列表 \n
    success: 操作是否成功 \n

    示例：\n
    mutation{
      getRandomDeadMemory(number:3){
        memorys{
          id,
          title,
          picture,
          audio,
          content,
          createTime,
          privacy,
          subjectId,
          subjectName
        },
        success
      }
    }
    """
    success = graphene.Boolean()
    memorys = graphene.List(MemoryType)

    class Arguments:
        number = graphene.Int()
        creatorUsername = graphene.String()

    def mutate(self, info, number=15, creatorUsername=''):
        if creatorUsername == '':
            memorys = Memory.objects.filter(activity=0,privacy=1).order_by('?')[:number]
        else:
            memorys = Memory.objects.filter(creatorUsername=creatorUsername, activity=0).order_by('?')[:number]
        return GetRandomDeadMemory(memorys=memorys, success=True)


class GetRandomAliveMemory(graphene.Mutation):
    """
    随机获取一批存活记忆

    参数: \n
    number: 获取数量(默认15条) \n
    creatorUsername: 创建者用户名(不填表示从所有用户的存活的公开记忆中获取) \n

    返回值: \n
    memorys： 获取到的记忆列表 \n
    success: 操作是否成功 \n

    示例：\n
    mutation{
      getRandomAliveMemory(number:3){
        memorys{
          id,
          title,
          picture,
          audio,
          content,
          createTime,
          privacy,
          subjectId,
          subjectName
        },
        success
      }
    }
    """
    success = graphene.Boolean()
    memorys = graphene.List(MemoryType)

    class Arguments:
        number = graphene.Int()
        creatorUsername = graphene.String()

    def mutate(self, info, number=15, creatorUsername=''):
        if creatorUsername == '':
            memorys = Memory.objects.filter(privacy=1).exclude(activity=0).order_by('?')[:number]
        else:
            memorys = Memory.objects.filter(creatorUsername=creatorUsername).exclude(activity=0).order_by('?')[:number]
        return GetRandomAliveMemory(memorys=memorys, success=True)


# class SetMemoryOwner(graphene.Mutation):
#     """
#     设置记忆所属(个人/集体)
#
#     参数: \n
#     memoryId!: 记忆编号 \n
#     category1!: 设置属于个人/集体(0/1) \n
#
#     返回值: \n
#     success: 操作是否成功 \n
#
#     示例：\n
#     mutation{
#       setMemoryOwner(memoryId:3, category1:1){
#         success
#       }
#     }
#     """
#     success = graphene.Boolean()
#
#     class Arguments:
#         memoryId = graphene.Int()
#         category1 = graphene.Int()
#
#     def mutate(self, info, memoryId, category1):
#         memory = Memory.objects.get(id=memoryId)
#         if memory.category1 == category1:
#             return SetMemoryOwner(success=False)
#         memory.category1 = category1
#         if category1 == 1:
#             subject = Subject.objects.create()
#             subject.name = memory.name
#             subject.save()
#             memory.subjectId = subject.id
#         else:
#             Subject.objects.get(id=memory.subjectId).delete()
#             memory.subjectId = None
#         memory.save()
#         return SetMemoryOwner(success=True)


class SetMemoryDensity(graphene.Mutation):
    """
    设置记忆私密度(私密/公开)

    参数: \n
    memoryId!: 记忆编号 \n
    privacy!: 设置私密度私密/公开(0/1) \n

    返回值: \n
    success: 操作是否成功 \n
    若失败则是因为私密度没有发生改变

    示例：\n
    mutation{
      setMemoryDensity(memoryId:3, category2:1){
        success
      }
    }
    """
    success = graphene.Boolean()

    class Arguments:
        memoryId = graphene.Int()
        privacy = graphene.Int()

    def mutate(self, info, memoryId, privacy):
        with transaction.atomic():
            memory = Memory.objects.get(id=memoryId)
            if memory.privacy == privacy:
                return SetMemoryDensity(success=False)
            memory.privacy = privacy
            memory.save()
            return SetMemoryDensity(success=True)


class MemoryMutation(graphene.ObjectType):
    create_memory = CreateMemory.Field()
    delete_memory = DeleteMemory.Field()
    get_all_memory = GetAllMemory.Field()
    search_memory = SearchMemory.Field()
    read_one_memory = ReadOneMemory.Field()
    get_random_dead_memory = GetRandomDeadMemory.Field()
    get_random_alive_memory = GetRandomAliveMemory.Field()
    # set_memory_owner = SetMemoryOwner.Field()
    set_memory_density = SetMemoryDensity.Field()