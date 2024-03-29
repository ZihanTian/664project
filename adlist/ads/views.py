from django.shortcuts import render

# Create your views here.
from ads.models import Ad, Comment

from django.views import View
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from ads.forms import CreateForm
from ads.forms import CommentForm
from ads.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse

from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
class AdListView(OwnerListView):
    model = Ad
    template_name = "ads/Ad_list.html"

class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = "ads/Ad_detail.html"
    def get(self, request, pk) :
        ad = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=ad).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'ad' : ad, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=f)
        comment.save()
        return redirect(reverse('ads:ad_detail', args=[pk])) 
class AdCreateView(LoginRequiredMixin, View):
    model = Ad
    fields = ['title', 'position','text', 'price']
    template = "ads/Ad_form.html"
   # template = 'pics/form.html'  #need to be changed later
    success_url = reverse_lazy('ads:ads')
    def get(self, request, pk=None) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        return redirect(self.success_url)
class AdUpdateView(LoginRequiredMixin, View):
    model = Ad
    fields = ['title', 'text']
    template = "ads/Ad_form.html"
   # template = 'pics/form.html'
    success_url = reverse_lazy('ads:ads')
    def get(self, request, pk) :
        pic = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=pic)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        pic = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        pic = form.save(commit=False)
        pic.save()

        return redirect(self.success_url)

class AdDeleteView(OwnerDeleteView):
    model = Ad
    template_name = "ads/Ad_delete.html"
class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ads/Ad_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        comment = self.object.ad
        return reverse('ads:ad_detail', args=[comment.id])

def stream_file1(request, pk) :
    pic = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type1'] = pic.content_type1
    response['Content-Length2'] = len(pic.picture1)
    response.write(pic.picture1)
    return response
def stream_file2(request, pk) :
    pic = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type2'] = pic.content_type2
    response['Content-Length2'] = len(pic.picture2)
    response.write(pic.picture2)
    return response
