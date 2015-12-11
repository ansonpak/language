from django.shortcuts import render , redirect
from wiki.models import Category, Page
from django.core.urlresolvers import reverse
from wiki.forms import CategoryForm, PageForm

def wiki(request):
    categories = Category.objects.order_by('-likes')
    context = {'categories':categories}
    return render(request, 'wiki/wiki.html', context)


def about(request):
    return render(request, 'wiki/about.html')

def category(request, categoryID):
    context = {}
    try:
        category = Category.objects.get(id=categoryID)
        context['category'] = category
        context['pages'] = Page.objects.filter(category=category)
    except Category.DoesNotExist:
        pass
    return render(request, 'wiki/category.html', context)


def addCategory(request):
    template = 'wiki/addCategory.html'
    if request.method=='GET':
        return render(request, template, {'form':CategoryForm()})
    # request.method=='POST'
    form = CategoryForm(request.POST)
    if not form.is_valid():
        return render(request, template, {'form':form})
    form.save()
    return redirect(reverse('wiki:wiki'))
    # Or try this: return wiki(request) 

def addPage(request, categoryID):
    template = 'wiki/addPage.html'
    try:
        pageCategory = Category.objects.get(id=categoryID)
    except Category.DoesNotExist:
        return category(request, categoryID)
    context = {'category':pageCategory}
    if request.method=='GET':
        context['form'] = PageForm()
        return render(request, template, context)
    # request.method=='POST'
    form = PageForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, template, context)
    page = form.save(commit=False)
    page.category = pageCategory
    page.save()
    return redirect(reverse('wiki:category', args=(categoryID, )))


def deleteCategory(request, categoryID):
    if request.method!='POST':
        return wiki(request)
    # request.method=='POST':
    categoryToDelete = Category.objects.get(id=categoryID)
    if categoryToDelete:
        categoryToDelete.delete()
    return redirect(reverse('wiki:wiki'))


def deletePage(request, pageID):
    if request.method!='POST':
        return wiki(request)
    # request.method=='POST':
    pageToDelete = Page.objects.get(id=pageID)
    if pageToDelete:
        categoryName = pageToDelete.category.id
        pageToDelete.delete()
    else:
        categoryName = ''
    return redirect(reverse('wiki:category', args=(categoryName, )))

def updateCategory(request, categoryID):
    template = 'wiki/updateCategory.html'
    try:
        categoryToUpdate = Category.objects.get(id=categoryID)
    except Category.DoesNotExist:
        return wiki(request)
    if request.method=='GET':
        form = CategoryForm(instance=categoryToUpdate)
        return render(request, template, {'form':form, 'category':categoryToUpdate})
    # request.method=='POST'
    form = CategoryForm(request.POST, instance=categoryToUpdate)
    if not form.is_valid():
        return render(request, template, {'form':form, 'category':categoryToUpdate})
    categoryToUpdate.save()
    return redirect(reverse('wiki:wiki'))

def updatePage(request, pageID):
    template = 'wiki/updatePage.html'
    try:
        page = Page.objects.get(id=pageID)
    except Page.DoesNotExist:
        return category(request, '')
    if request.method=='GET':
        form = PageForm(instance=page)
        return render(request, template, {'form':form, 'page':page})
    # request.method=='POST'
    form = PageForm(request.POST, instance=page)
    if not form.is_valid():
        return render(request, template, {'form':form, 'page':page})
    page.save()
    return redirect(reverse('wiki:category', args=(page.category.id,)))