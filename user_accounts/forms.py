from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, CompanyProfile, CustomerProfile, Customer
from django.core.exceptions import ValidationError
from product_catalog.models import ProductCategory

class CompanyProfileForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=20,
        label=_('رقم الهاتف'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CompanyProfile
        fields = ('company_name', 'category', 'location', 'city', 'bio', 'logo', 'baner', 'website')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control location-field', 'readonly': 'readonly'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'baner': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['phone_number'].initial = self.instance.user.phone_number

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # Update the user's phone number
            if instance.user:
                instance.user.phone_number = self.cleaned_data['phone_number']
                instance.user.save()
        return instance

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('store_name', 'phone', 'address', 'city', 'country', 'location')
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control location-field', 'readonly': 'readonly'}),
            'store_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'store_name': _('اسم المتجر'),
            'phone': _('رقم الهاتف'),
            'address': _('العنوان'),
            'city': _('المدينة'),
            'country': _('البلد'),
            'location': _('الموقع'),
        }

class RegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=[('company', _('شركة')), ('customer', _('متجر'))],
        widget=forms.RadioSelect(attrs={'class': 'invisible'}),
        label=_('نوع الحساب')
    )
    
    # Company fields
    company_name = forms.CharField(
        max_length=100,
        label=_('اسم الشركة'),
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        queryset=ProductCategory.objects.all(),
        label=_('صنف الشركة'),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    website = forms.URLField(
        required=False,
        label=_('الموقع الإلكتروني'),
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )
    
    # Customer fields
    store_name = forms.CharField(
        max_length=100,
        label=_('اسم المتجر'),
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    # Common fields
    phone_number = forms.CharField(
        max_length=20,
        label=_('رقم الهاتف'),
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    city = forms.CharField(
        max_length=100,
        label=_('المدينة'),
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    location = forms.CharField(
        max_length=255,
        label=_('الموقع'),
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control location-field'})
    )
    latitude = forms.FloatField(
        required=False,
        widget=forms.HiddenInput(),
        initial=0.0
    )
    longitude = forms.FloatField(
        required=False,
        widget=forms.HiddenInput(),
        initial=0.0
    )
    bio = forms.CharField(
        label=_('نبذة تعريفية'),
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    logo = forms.ImageField(
        required=True,
        label=_('الشعار'),
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        help_text=_('قم بتحميل شعار لشركتك/متجرك')
    )
    baner = forms.ImageField(
        required=True,
        label=_('البنر'),
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        help_text=_('قم بتحميل بنر لشركتك/متجرك')
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'user_type', 'phone_number', 'city', 'location', 'bio', 'logo', 'baner')
        labels = {
            'username': _('اسم المستخدم'),
            'email': _('البريد الإلكتروني'),
            'password1': _('كلمة المرور'),
            'password2': _('تأكيد كلمة المرور'),
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'username': _('مطلوب. 150 حرف أو أقل. أحرف وأرقام و @/./+/-/_ فقط.'),
            'password1': _('يجب أن تحتوي كلمة المرور على 8 أحرف على الأقل وتتضمن أحرف وأرقام.'),
        }
        error_messages = {
            'username': {
                'unique': _('اسم المستخدم هذا مستخدم بالفعل.'),
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If the form is bound (POST request)
        if args and args[0]:
            user_type = args[0].get('user_type')
            if user_type == 'company':
                self.fields['company_name'].required = True
                self.fields['category'].required = True
                self.fields['store_name'].required = False
            elif user_type == 'customer':
                self.fields['store_name'].required = True
                self.fields['company_name'].required = False
                self.fields['category'].required = False

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("حقول كلمة المرور غير متطابقة."))
        if len(password1) < 8:
            raise forms.ValidationError(_("يجب أن تكون كلمة المرور 8 أحرف على الأقل."))
        if password1.isdigit():
            raise forms.ValidationError(_("لا يمكن أن تكون كلمة المرور أرقامًا فقط."))
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError(_("يجب أن تحتوي كلمة المرور على رقم واحد على الأقل."))
        return password2

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        
        if user_type == 'company':
            company_name = cleaned_data.get('company_name')
            if not company_name:
                self.add_error('company_name', _('اسم الشركة مطلوب لحسابات الشركات.'))
        
        elif user_type == 'customer':
            store_name = cleaned_data.get('store_name')
            if not store_name:
                self.add_error('store_name', _('اسم المتجر مطلوب لحسابات المتاجر.'))
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data['user_type']
        user.phone_number = self.cleaned_data['phone_number']
        user.save()

        if user.user_type == 'company':
            profile = CompanyProfile(
                user=user,
                company_name=self.cleaned_data['company_name'],
                category=self.cleaned_data['category'],
                location=self.cleaned_data['location'],
                city=self.cleaned_data['city'],
                bio=self.cleaned_data['bio'],
                website=self.cleaned_data['website'],
                logo=self.cleaned_data['logo'],
                baner=self.cleaned_data['baner']
            )
            if self.cleaned_data.get('logo'):
                profile.logo = self.cleaned_data['logo']
            try:
                profile.save()
            except Exception as e:
                user.delete()
                raise ValidationError(_('Error creating company profile: %s') % str(e))
        elif user.user_type == 'customer':
            profile = Customer(
                user=user,
                store_name=self.cleaned_data['store_name'],
                phone=self.cleaned_data['phone_number'],
                address=self.cleaned_data['location'],
                city=self.cleaned_data['city'],
                country='IQ',  # Default to Iraq
                location=self.cleaned_data['location']
            )
            try:
                profile.save()
            except Exception as e:
                user.delete()
                raise ValidationError(_('Error creating customer profile: %s') % str(e))

        return user 

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to the form fields
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'أدخل كلمة المرور الحالية',
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'أدخل كلمة المرور الجديدة',
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'أكد كلمة المرور الجديدة',
        }) 