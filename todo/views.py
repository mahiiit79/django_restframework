from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Todo
from .serializers import TodoSerializer,UserSerializer
from rest_framework import status,viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins,generics
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

User = get_user_model()

#region function baseview
#CRUD
@api_view(['GET','POST'])
def all_todos(request: Request):
    if request.method == 'GET':
        todos = Todo.objects.order_by('priority').all()
        #if instance = todos pas bedi behesh just select mikone
        todo_serializer = TodoSerializer(todos, many=True)
        return Response(todo_serializer.data, status.HTTP_200_OK)
    # وقتی مقدار تودوز رو پاس میدیم به سریالایزر مقدار دیتا رو پر میکنه درواقع دیتا بهش اضافه میشه
    elif request.method == 'POST':
        #اینحا میایم اون جی سان رو به فرمت جنگو درمیاریم درواقع دی سریالایز میکنیم
        # if data pas bedi save mikone
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
    return Response(None,status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def todo_detail_view(request:Request,todo_id:int):
    # todo = Todo.objects.filter(pk=todo_id).first()
    try:
        todo = Todo.objects.get(pk=todo_id)
    except Todo.DoesNotExist:
        return Response(None,status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        return Response(serializer.data,status.HTTP_200_OK)
    #if data & instance to do ro negah midare data deserialize mikone mirize dakhel to do
    elif request.method == 'PUT':
        serializer = TodoSerializer(todo,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_202_ACCEPTED)
        return Response(None,status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        todo.delete()
        return Response(None,status.HTTP_204_NO_CONTENT)
#endregion


#region class baseview
class TodosListApiView(APIView):
    @extend_schema(
        request=TodoSerializer,
        responses={201: TodoSerializer},
        description='this api is used for get all todos list',)

    def get(self,request:Request):
        todos = Todo.objects.order_by('priority').all()
        todo_serializer = TodoSerializer(todos, many=True)
        return Response(todo_serializer.data, status.HTTP_200_OK)

    def post(self,request:Request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(None,status.HTTP_400_BAD_REQUEST)

class TodosDetailApiView(APIView):
    def get_object(self,todo_id:int):
        try:
            todo = Todo.objects.get(pk=todo_id)
            return todo
        except Todo.DoesNotExist:
            return Response(None, status.HTTP_404_NOT_FOUND)

    def get(self,request:Request,todo_id:int):
        todo = self.get_object(todo_id)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request: Request, todo_id:int):
        todo = self.get_object(todo_id)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
        return Response(None, status.HTTP_400_BAD_REQUEST)

    def delete(self,request:Request,todo_id:int):
        todo = self.get_object(todo_id)
        todo.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)


#endregion classbase view


#region mixins
class TodosListMixinApiView(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    def get(self,request:Request):
        return self.list(request)
    def post(self,request:Request):
        return self.create(request)


class TodosDetailMixinApiView(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    def get(self,request:Request,pk):
        return self.retrieve(request,pk)
    def put(self,request:Request,pk):
        return self.update(request,pk)
    def delete(self,request,pk):
        return self.destroy(request,pk)
#endregion

#region generics
#ListCreateAPIView ham select mikone ham misaze
class TodoGenericApiView(generics.ListCreateAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    pagination_class = PageNumberPagination
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]


class TodosGenericDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer



#endregion


#region viewSets
class TodoViewSetApiView(viewsets.ModelViewSet):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    pagination_class = LimitOffsetPagination


#endregion


#regions users
class UsersGenericApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


#endregion