from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from . import forms
from . import models
from django.shortcuts import get_object_or_404
from django.forms import formset_factory


@login_required
def home(request):
    photos = models.Photo.objects.all()
    reviews = models.Review.objects.all()
    return render(request, 'reviews/home.html', context={'photos': photos, 'reviews': reviews})


@login_required
def photo_upload(request):
    form = forms.PhotoForm()
    if request.method == 'POST':
        form = forms.PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            # set the uploader to the user before saving the model
            photo.uploader = request.user
            # now we can save
            photo.save()
            return redirect('home')
    return render(request, 'reviews/photo_upload.html', context={'form': form})


@login_required
def review_and_photo_upload(request):
    review_form = forms.ReviewForm()
    photo_form = forms.PhotoForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if all([review_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            review = review_form.save(commit=False)
            review.author = request.user
            review.photo = photo
            review.save()
            return redirect('home')
    context = {
        'review_form': review_form,
        'photo_form': photo_form,
    }
    return render(request, 'reviews/create_review_post.html', context=context)


@login_required
def view_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    return render(request, 'reviews/view_review.html', {'review': review})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    edit_form = forms.ReviewForm(instance=review)
    delete_form = forms.DeleteReviewForm()
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_form = forms.ReviewForm(request.POST, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_review' in request.POST:
            delete_form = forms.DeleteReviewForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect('home')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'reviews/edit_review.html', context=context)


@login_required
def create_multiple_photos(request):
    PhotoFormSet = formset_factory(forms.PhotoForm, extra=5)
    formset = PhotoFormSet()
    if request.method == 'POST':
        formset = PhotoFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    photo = form.save(commit=False)
                    photo.uploader = request.user
                    photo.save()
            return redirect('home')
    return render(request, 'reviews/create_multiple_photos.html', {'formset': formset})