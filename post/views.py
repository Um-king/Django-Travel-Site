from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DeleteView,
    UpdateView,
    DetailView,
    CreateView,
)
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, Favorite, Tag
from .forms import CommentForm, PostForm

# from .forms import PostForm, CommentForm
from django.urls import reverse_lazy
from datetime import date
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404


import pickle
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.http import HttpResponseRedirect
from django.conf import settings

import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

class PostListView(ListView):
    model = Post
    template_name = "post_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("q", "")
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(contents__icontains=search_query)
                | Q(category__icontains=search_query)
                | Q(tags__name__icontains=search_query)
            ).distinct().order_by("-createDate")
        else:
            queryset = Post.objects.all().order_by("-createDate")
        return queryset

    # context의 값을 지정하기 위한 오버라이딩
    def get_context_data(self, **kwargs):
        # 기존 컨텍스트 데이터를 가져오기
        context = super().get_context_data(**kwargs)
        # 10번 반복을 위한 범위 추가
        context["repeat_times"] = range(10)

        search_query = self.request.GET.get("q", "")
        context["search_query"] = search_query  # 검색어를 저장합니다.
        # context['object_list']는 get_queryset 메서드에 의해 이미 설정되었습니다.

        if self.request.user.is_authenticated:
            # 현재 사용자의 포스트만 필터링
            user_posts = self.get_queryset().filter(author=self.request.user)
            context["user_posts"] = user_posts

            # 현재 사용자의 즐겨찾기 목록을 가져옵니다.
            favorites = Favorite.objects.filter(user=self.request.user).values_list('post_id', flat=True)
            context['favorites'] = favorites

        return context


post_list = PostListView.as_view()


class lst:
    lst_name = ""


lst_name = lst()


def post_detail_list(request):
    q = request.GET.get("q", "")
    q_search = request.GET.get("q_search", "")   
    order = request.GET.get("order", "latest")

    if q != "":
        lst_name.lst_name = q


    if lst_name.lst_name == "all_list":
        posts = Post.objects.all().order_by("-createDate")
    else:
        posts = Post.objects.filter(author=request.user).order_by("-createDate")

    if q_search:
        posts = (
            posts.filter(
                Q(title__icontains=q_search)
                | Q(contents__icontains=q_search)
                | Q(category__icontains=q_search)
                | Q(tags__name__icontains=q_search)
            )
            .distinct()
            .order_by("-createDate")
        )

     # 정렬 순서를 적용합니다.
    if order == "views":
        posts = posts.order_by("-count")
    elif order == "favorites" and request.user.is_authenticated:
        posts = posts.filter(favorite__user=request.user)
    else:
        posts = posts.order_by("-createDate")  # 'latest'의 경우 또는 order 매개변수가 주어지지 않았을 때
    
    favorites = Favorite.objects.filter(user=request.user).values_list('post', flat=True)
    context = {
        "object_list": posts,
        "favorites": favorites,
        "order":order,
    }
    return render(request, "post/post_detail_list.html", context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "post/post_create.html"
    success_url = reverse_lazy("post_detail_list")  # 포스트 작성 성공 후 리다이렉트 될 URL
    login_url = reverse_lazy(
        "user_login"
    )  # 로그인하지 않은 사용자를 위한 로그인 페이지 URL

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user  # Post의 author 필드를 현재 사용자로 설정합니다.
        self.object.save()  # 변경 사항을 데이터베이스에 저장합니다.

        # 태그 처리
        tags_str = form.cleaned_data.get('tags', '')
        if tags_str:
            tags_list = [tag_name.strip() for tag_name in tags_str.split(',')]
            tags=[]
            for tag_name in tags_list:
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    tags.append(tag)

            self.object.tags.set(tags)
            self.object.save()
        return super().form_valid(form)

        # # 태그 처리
        # tags_str = form.cleaned_data.get('tags', '')
        # if tags_str:
        #     tags_list = [tag_name.strip() for tag_name in tags_str.split(',')]
        #     for tag_name in tags_list:
        #         if tag_name:
        #             # 존재하는 Tag 인스턴스만 검색
        #             tag = Tag.objects.filter(name=tag_name).first()
        #             if tag:
        #                 # 존재하는 Tag 인스턴스와 Post 인스턴스를 연결
        #                 self.object.tags.add(tag)

        # return super().form_valid(form)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = date.today()  # 오늘 날짜를 컨텍스트에 추가
        return context

    


post_create = PostCreateView.as_view()


class PostDetailView(DetailView):
    model = Post
    # context_object_name = 'licat_objects' # {{licat_objects.title}} 이런식으로 사용 가능
    template_name = "post/post_detail.html"

    def get_context_data(self, **kwargs):
        """
        여기서 원하는 쿼리셋이나 object를 추가한 후 템플릿으로 전달할 수 있습니다.
        """
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()  # 댓글 폼을 컨텍스트에 추가

        # 즐겨찾기 상태를 확인하여 컨텍스트에 추가
        if self.request.user.is_authenticated:
            is_favorite = Favorite.objects.filter(user=self.request.user, post=self.object).exists()
            context["is_favorite"] = is_favorite
        else:
            context["is_favorite"] = False
            
        return context

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        try:
            # get_object_or_404를 사용하여 Post 객체를 가져옵니다.
            post = get_object_or_404(Post, pk=pk)
            # Post 객체가 존재하면, 조회수를 1 증가시키고 저장합니다.
            post.count += 1
            post.save()
            return post  # 수정된 Post 객체를 반환합니다.
        except Http404:
            # Post 객체가 존재하지 않을 경우, 사용자에게 메시지를 보내고 리스트 페이지로 리다이렉트합니다.
            messages.error(self.request, "해당 게시글은 삭제되었습니다.")
            return redirect(
                "post_detail_list"
            )  # 여기서 'post_list'는 게시글 리스트를 보여주는 뷰의 URL name입니다.

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                author=request.user,
                message=form.cleaned_data["message"],
                post=self.object,
            )
            # 폼이 유효하면, 게시글 상세 페이지로 리다이렉트합니다.
            return HttpResponseRedirect(self.object.get_absolute_url())

        # 폼이 유효하지 않을 경우, 기존 로직을 따릅니다.
        context = self.get_context_data(object=self.object)
        context["comment_form"] = form
        return self.render_to_response(context)

    # def get_object(self, queryset=None): # 쿼리셋을 어떻게 할거냐 -> 요청이 왔을때 -> object를 가져오는 것
    #     pk = self.kwargs.get('pk')
    #     post = Post.objects.get(pk=pk) # 해당 pk의 object를 가져온다.
    #     post.count += 1
    #     post.save()
    #     return super().get_object(queryset)


post_detail = PostDetailView.as_view()


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("post_detail_list")
    template_name = "post/post_create.html"

    def test_func(self):  # test_func이라는 함수명 자체가 필수 구현해야하는 함수
        obj = self.get_object()
        return obj.author == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = date.today()  # 오늘 날짜를 컨텍스트에 추가
        return context


post_update = PostUpdateView.as_view()


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post_detail_list")

    def test_func(
        self,
    ):  # UserPassesTestMixin에 있고 test_func() 메서드를 오버라이딩, True, False 값으로 접근 제한
        return self.get_object().author == self.request.user


post_delete = PostDeleteView.as_view()




from .forms import TravelerForm
from .models import Area  # 여행지 정보가 저장된 모델
import pandas as pd
import os


# 모델 로드 함수
def load_model():
    model_path = os.path.join(settings.MODEL_ROOT, 'model.pkl')  # settings.MODEL_ROOT는 settings.py에 정의해야 합니다.
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

def predict_view(request):
    # 모델 인스턴스 로드
    model = load_model()

    if request.method == "POST":
        form = TravelerForm(request.POST)
        if form.is_valid():
            # 폼 데이터를 여행자 정보 사전 형태로 변환
            traveler_data = form.cleaned_data
            traveler = {
                'GENDER': traveler_data.get('GENDER'),
                'AGE_GRP': traveler_data.get('AGE_GRP'),
                'TRAVEL_STYL_1': traveler_data.get('TRAVEL_STYL_1'),
                'TRAVEL_STYL_2': traveler_data.get('TRAVEL_STYL_2'),
                'TRAVEL_STYL_3': traveler_data.get('TRAVEL_STYL_3'),
                'TRAVEL_STYL_4': traveler_data.get('TRAVEL_STYL_4'),
                'TRAVEL_STYL_5': traveler_data.get('TRAVEL_STYL_5'),
                'TRAVEL_STYL_6': traveler_data.get('TRAVEL_STYL_6'),
                'TRAVEL_STYL_7': traveler_data.get('TRAVEL_STYL_7'),
                'TRAVEL_STYL_8': traveler_data.get('TRAVEL_STYL_8'),
                'TRAVEL_MOTIVE_1': traveler_data.get('TRAVEL_MOTIVE_1'),
                'TRAVEL_COMPANIONS_NUM': traveler_data.get('TRAVEL_COMPANIONS_NUM'),
                'TRAVEL_MISSION_INT': traveler_data.get('TRAVEL_MISSION_INT'),
            }
            
            # 여행지 목록을 데이터베이스에서 가져옴
            area_names = Area.objects.all().values_list('name', flat=True)
            
            # 결과를 저장할 빈 데이터프레임 초기화
            results = pd.DataFrame([], columns=['AREA', 'SCORE'])
            
            for area in area_names:
                input_data = list(traveler.values()) + [area]  # 입력 데이터 준비
                score = model.predict([input_data])[0]  # 점수 예측
                
                # 결과 데이터프레임에 지역과 점수 추가
                results = pd.concat([results, pd.DataFrame([[area, score]], columns=['AREA', 'SCORE'])])
            
            # 결과 정렬 및 상위 10개 선택
            top_results = results.sort_values('SCORE', ascending=False).head(10)
            print(len(top_results))
            print(traveler_data.get('GENDER'))
            
            # 템플릿에 결과 전달
            return render(request, "post/predict_result.html", {"results": top_results.to_dict('records')})
    else:
        form = TravelerForm()

    return render(request, "post/predict_form.html", {"form": form})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # 댓글 작성자와 요청을 보낸 사용자가 동일한지 확인
    if comment.author != request.user:
        return HttpResponseForbidden()  # 권한이 없는 경우 403 에러 반환
    
    post_id = comment.post.id  # 삭제 후 리다이렉트할 포스트의 ID를 저장
    comment.delete()  # 댓글 삭제
    return redirect('post_detail', pk=post_id)


@login_required
def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, author=request.user)
    
    # POST 요청인 경우에만 처리
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "댓글이 업데이트되었습니다.")
            return redirect(comment.post.get_absolute_url())
        else:
            # 폼이 유효하지 않으면 오류 메시지와 함께 댓글이 달린 포스트로 리다이렉션
            messages.error(request, "댓글 업데이트에 실패했습니다.")
    else:
        form = CommentForm(instance=comment)

    # GET 요청인 경우 또는 폼이 유효하지 않은 경우, 포스트 상세 페이지로 리다이렉션
    return redirect(comment.post.get_absolute_url())


@login_required
def add_reply(request, comment_id):
    parent_comment = get_object_or_404(Comment, pk=comment_id) # 부모 댓글 객체를 찾습니다.
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.post = parent_comment.post # 대댓글의 post는 부모 댓글의 post와 동일합니다.
            reply.parent = parent_comment # 부모 댓글을 설정합니다.
            reply.save()
            return redirect('post_detail', pk=reply.post.pk) # 대댓글이 추가된 글의 상세 페이지로 리다이렉트합니다.
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'form': form})

@login_required
def toggle_favorite(request, pk):
    post = get_object_or_404(Post, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, post=post)

    if not created:
        favorite.delete()  # 이미 즐겨찾기 되어 있으면 제거
    else:
        # 새로 생성된 경우는 이미 save()가 호출되었으므로 추가 동작이 필요하지 않습니다.
        pass

    # 즐겨찾기를 토글한 후에 게시글 상세 페이지로 리다이렉트합니다.
    return redirect('post_detail', pk=pk)



@csrf_exempt
def get_ai_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data['message']
        
        # 프롬프트 설정
        prompt = f"""
        안녕, 너는 대한민국 전국 곳곳을 다녀온 여행 전문가야. 
        사용자가 너와 대화를 시작하면 너는 사용자의 나이와 여행 스타일을 질문하고 
        제목과 컨텐츠, 상세 일정, 여행지 미션, 기타사항(뉴스, 사이트 및 참고 사항)을 추천해주면 돼.

        결과는 사용자가 "질문 완료"를 입력하면 결과를 보내주면 돼.
        각각의 카테고리 별로 나눠서 Json 형식으로 주면 좋겠어. 
        
        인사말, 마무리말 필요없이 마지막 답변은 항상 이렇게만 작성해
        {{
            'title' : 제목,
            'Content' : 내용,
            'date' : 일정에 대한 스케줄,
            'mission' : 여행지에 대한 퀘스트,
            'etc' : 기타사항
        }}
        """
        
        # 사용자의 메시지: "{user_message}"
        # 사용자가 질문을 완료했습니다. 추천을 시작해주세요.
        
        # OpenAI API 호출
        openai.api_key = ''
        # response = openai.Completion.create(
        #   engine="gpt-3.5-turbo",
        #   prompt=prompt,
        #   temperature=0.7,
        #   max_tokens=50,
        #   top_p=1,
        #   frequency_penalty=0,
        #   presence_penalty=0
        # )

        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {'role': 'system', 'content': prompt},
                    {'role': 'user', 'content': user_message}
                ]
            )
        
        # 대화형 API 응답에서 메시지 내용 추출
        if 'choices' in response and len(response['choices']) > 0:
            message_content = response['choices'][0]['message']['content']
            if(str(message_content).find('{') != -1):
                msg = str(message_content).split('{')[1]
                msg = '{' + msg
                return JsonResponse({"answer": msg.replace('\'', '\"')})
            return JsonResponse({"answer": message_content})
            
        else:
            message_content = "I couldn't get a response. Please try again."
            return JsonResponse({"answer": message_content})
