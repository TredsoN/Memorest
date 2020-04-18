import graphene
from graphene_django import DjangoObjectType
from graphene import ObjectType, String, Schema

from memory.models import Memory, Subject


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
    name = graphene.String(required=True)
    creatorId = graphene.Int(required=True)
    picture = graphene.String(required=True)
    audio = graphene.String(required=True)
    content = graphene.String(required=True)
    category1 = graphene.Int(required=True)
    category2 = graphene.Int(required=True)


class CreateMemory(graphene.Mutation):
    """
    创建记忆

    参数: \n
    name!: 记忆名字 \n
    creatorId!: 创建人编号 \n
    picture!: 图片文件地址 \n
    audio!: 音频文件地址 \n
    content!: 记忆内容 \n
    category1!: 个人/集体记忆(0/1) \n
    category2!: 私密/公开记忆(0/1) \n

    返回值: \n
    success: 操作是否成功 \n

    示例：\n
    mutation createMemory{
        createMemory(memoryData:{name:"memory1", creatorId:3, picture:"",audio:"",content:"this is one memory", category1:1,category2:0}){
        success
        }
    }
    """
    success = graphene.Boolean()

    class Arguments:
        memory_data = MemoryInput(required=True)

    def mutate(self, info, memory_data):
        memory = Memory.objects.create()
        memory.name = memory_data['name']
        memory.creatorId = memory_data['creatorId']
        if memory_data['category1'] == 1:
            subject = Subject.objects.create()
            subject.name = memory_data['name']
            subject.save()
            memory.subjectId = subject.id
        memory.picture = memory_data['picture']
        memory.audio = memory_data['audio']
        memory.content = memory_data['content']
        memory.category1 = memory_data['category1']
        memory.category2 = memory_data['category2']
        memory.save()
        return CreateMemory(success=True)


class GetAllMemory(graphene.Mutation):
    """
    获取所有记忆

    参数: \n
    creatorId: 用户编号(不填则表示获取所有用户的所有记忆) \n
    aliveOnly： 仅获取存活的记忆(默认为True) \n

    返回值: \n
    memorys： 该用户创建的所有的记忆 \n
    success: 操作是否成功 \n

    示例：\n
    mutation{
      getAllMemory(creatorId:3){
        memorys{
          id,
          name,
          picture,
          audio,
          content,
          createTime
        },
        success
      }
    }
    """
    success = graphene.Boolean()
    memorys = graphene.List(MemoryType)

    class Arguments:
        creatorId = graphene.Int()
        aliveOnly = graphene.Boolean()

    def mutate(self, info, creatorId=0, aliveOnly=True):
        if creatorId == 0:
            memorys = Memory.objects.all()
        else:
            memorys = Memory.objects.filter(creatorId=creatorId)
        if aliveOnly:
            memorys = memorys.exclude(activity=0)
        return GetAllMemory(memorys=memorys, success=True)


class ReadOneMemory(graphene.Mutation):
    """
    查看某条记忆

    参数: \n
    memoryId!: 记忆编号 \n

    返回值: \n
    memory： 该条记忆的信息 \n
    success: 操作是否成功 \n

    示例：\n
    mutation{
      readOneMemory(memoryId:3){
        memory{
          id,
          name,
          picture,
          audio,
          content,
          createTime
        },
        success
      }
    }
    """
    success = graphene.Boolean()
    memory = graphene.Field(MemoryType)

    class Arguments:
        memoryId = graphene.Int(required=True)

    def mutate(self, info, memoryId):
        memory = Memory.objects.get(id=memoryId)
        return ReadOneMemory(memory=memory, success=True)


class GetRandomDeadMemory(graphene.Mutation):
    """
    随机获取一批死去记忆

    参数: \n
    number: 获取数量(默认5条) \n
    creatorId: 创建者编号(不填表示从所有用户的死去的公开记忆中获取) \n

    返回值: \n
    memorys： 获取到的记忆列表 \n
    success: 操作是否成功 \n

    示例：\n
    mutation{
      getRandomDeadMemory(number:3){
        memorys{
          id,
          name,
          picture,
          audio,
          content,
          createTime
        },
        success
      }
    }
    """
    success = graphene.Boolean()
    memorys = graphene.List(MemoryType)

    class Arguments:
        number = graphene.Int()
        creatorId = graphene.Int()

    def mutate(self, info, number=5, creatorId=0):
        if creatorId == 0:
            memorys = Memory.objects.filter(activity=0,category2=1).order_by('?')[:number]
        else:
            memorys = Memory.objects.filter(id=creatorId, activity=0).order_by('?')[:number]
        return GetRandomDeadMemory(memorys=memorys, success=True)


class GetRandomAliveMemory(graphene.Mutation):
    """
    随机获取一批存活记忆

    参数: \n
    number: 获取数量(默认5条) \n
    creatorId: 创建者编号(不填表示从所有用户的存活的公开记忆中获取) \n

    返回值: \n
    memorys： 获取到的记忆列表 \n
    success: 操作是否成功 \n

    示例：\n
    mutation{
      getRandomAliveMemory(number:3){
        memorys{
          id,
          name,
          picture,
          audio,
          content,
          createTime
        },
        success
      }
    }
    """
    success = graphene.Boolean()
    memorys = graphene.List(MemoryType)

    class Arguments:
        number = graphene.Int()
        creatorId = graphene.Int()

    def mutate(self, info, number=5, creatorId=0):
        if creatorId == 0:
            memorys = Memory.objects.filter(category2=1).exclude(activity=0).order_by('?')[:number]
        else:
            memorys = Memory.objects.filter(id=creatorId).exclude(activity=0).order_by('?')[:number]
        return GetRandomAliveMemory(memorys=memorys, success=True)


class SetMemoryOwner(graphene.Mutation):
    """
    设置记忆所属(个人/集体)

    参数: \n
    memoryId!: 记忆编号 \n
    category1!: 设置属于个人/集体(0/1) \n

    返回值: \n
    success: 操作是否成功 \n

    示例：\n
    mutation{
      setMemoryOwner(memoryId:3, category1:1){
        success
      }
    }
    """
    success = graphene.Boolean()

    class Arguments:
        memoryId = graphene.Int()
        category1 = graphene.Int()

    def mutate(self, info, memoryId, category1):
        memory = Memory.objects.get(id=memoryId)
        if memory.category1 == category1:
            return SetMemoryOwner(success=False)
        memory.category1 = category1
        if category1 == 1:
            subject = Subject.objects.create()
            subject.name = memory.name
            subject.save()
            memory.subjectId = subject.id
        else:
            Subject.objects.get(id=memory.subjectId).delete()
            memory.subjectId = None
        memory.save()
        return SetMemoryOwner(success=True)


class SetMemoryDensity(graphene.Mutation):
    """
    设置记忆私密度(私密/公开)

    参数: \n
    memoryId!: 记忆编号 \n
    category2!: 设置私密度私密/公开(0/1) \n

    返回值: \n
    success: 操作是否成功 \n

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
        category2 = graphene.Int()

    def mutate(self, info, memoryId, category2):
        memory = Memory.objects.get(id=memoryId)
        if memory.category2 == category2:
            return SetMemoryDensity(success=False)
        memory.category2 = category2
        memory.save()
        return SetMemoryDensity(success=True)


class MemoryMutation(graphene.ObjectType):
    create_memory = CreateMemory.Field()
    get_all_memory = GetAllMemory.Field()
    read_one_memory = ReadOneMemory.Field()
    get_random_dead_memory = GetRandomDeadMemory.Field()
    get_random_alive_memory = GetRandomAliveMemory.Field()
    set_memory_owner = SetMemoryOwner.Field()
    set_memory_density = SetMemoryDensity.Field()
