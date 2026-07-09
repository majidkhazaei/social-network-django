from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegisterForm, UserLoginForm, EditUserForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from .models import Relation, Profile


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'account/user_register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request,'ثبت نام با موفقیت انجام شد.', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/user_login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request,"ورود با موفقیت انجام شد.", 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request,'نام کاربری یا رمز عبور اشتباه است!', 'danger')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        messages.success(request,'با موفقیت از حساب کاربری خود خارج شدید', 'success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin,View):
    def get(self, request, user_id):
        is_following = False
        user = User.objects.get(pk=user_id)
        posts = user.posts.all()
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        return render(request, 'account/user_profile.html', {'user': user,'posts': posts, 'is_following': is_following})


class UserFollowView(LoginRequiredMixin,View):
    def get(self, request, user_id):
        user =  User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user= user).exists()
        if relation:
            messages.error(request, f'you already followed {user.username}', 'danger')
        else:
            Relation(from_user=request.user, to_user=user).save()
            messages.success(request, f'you are following {user.username}', 'success')
        return redirect('account:user_profile', user_id)



class UserUnfollowView(LoginRequiredMixin,View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, f'you are unfollowed {user.username}', 'success')
        else:
            messages.error(request, f'you are not following {user.username}', 'danger')
        return redirect('account:user_profile', user_id)


class EditUserView(LoginRequiredMixin,View):
    form_class = EditUserForm

    def get(self, request):
        form = self.form_class(instance=request.user.profile, initial={'email': request.user.email})
        return render(request, 'account/user_edit.html',{'form':form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data.get('email')
            request.user.save()
            messages.success(request,'profile updated successfully', 'success')
        return redirect('account:user_profile', request.user.id)



#API VIEWS
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, ProfileSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.throttling import  AnonRateThrottle
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

@extend_schema(
    summary="Register User",
    description="Create a new user account using username, email, and password.",
    tags=["Auth"],
    request=UserRegisterSerializer,
    responses={201: UserRegisterSerializer},
)
class UserRegisterAPI(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Follow / Unfollow User",
    description="Toggle follow status of a user.",
    tags=["Users"],
    request=None,
    responses={200: {"type": "object", "properties": {"message": {"type": "string"}}}},
)
class FollowToggleAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user.id == user_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        rel = Relation.objects.filter(from_user=request.user, to_user=user)
        if rel:
            rel.delete()
            return Response({"message": "unfollowed"}, status=status.HTTP_200_OK)
        else:
            Relation.objects.create(from_user=request.user, to_user=user)
            return Response({"message": "followed"}, status=status.HTTP_200_OK)

@extend_schema_view(
    get=extend_schema(
        summary="Get Current User Profile",
        description="Retrieve profile of the authenticated user.",
        tags=["Profile"],
    ),
    put=extend_schema(
        summary="Update Profile",
        description="Update profile information.",
        tags=["Profile"],
    ),
    patch=extend_schema(
        summary="Partial Update Profile",
        tags=["Profile"],
    )
)
class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


@extend_schema(
    summary="List All Users",
    description="Retrieve list of all users (for authenticated users).",
    tags=["Users"],
)
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['date_joined']
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    search_fields = ['username',]
