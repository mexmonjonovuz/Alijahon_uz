import re

from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import CharField, ModelChoiceField, ModelForm, PasswordInput
from django.utils.translation import gettext_lazy as _

from .models import User, Product, Stream
from .models.shop import Order, Favorite, Transaction


class CustomAdminAuthenticationForm(AdminAuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["username"].widget.attrs["maxlength"] = 25

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return re.sub(r'[^\d]', '', username)[-9:]


class UserAuthenticatedForm(ModelForm):
    phone = CharField()
    password = CharField(
        label="Password",
        strip=False,
        widget=PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    error_messages = {
        "invalid_login":
            "Please enter a correct %(phone)s and password. Note that both "
            "fields may be case-sensitive."
        ,
        "inactive": "This account is inactive.", }

    class Meta:
        model = User
        fields = 'phone', 'password'

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean_phone(self):
        phone = self.data.get('phone')
        return re.sub(r'[^\d]', '', phone)[-9:]

    def clean(self):
        phone = self.cleaned_data.get("phone")
        password = self.cleaned_data.get("password")

        if phone is not None and password:
            if not User.objects.filter(phone=phone).exists():
                self.user_cache = User.objects.create_user(phone=phone, password=password)
            else:
                self.user_cache = authenticate(
                    self.request, phone=phone, password=password
                )
            if self.user_cache is None:
                raise ValidationError(self.error_messages["inactive"],
                                      code="inactive")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache


class UserSettingsForm(ModelForm):
    class Meta:
        model = User
        fields = 'first_name', 'address', 'telegram_id', 'bio', 'district', 'last_name', 'image'


class UserChangePasswordForm(ModelForm):
    password1 = CharField(max_length=255, label='Yangi Parol', widget=PasswordInput)
    password2 = CharField(max_length=255, label='Yangi Parolni Tasdiqlash', widget=PasswordInput)

    class Meta:
        model = User
        fields = 'password', 'password1', 'password2'

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not self.instance.check_password(password):
            raise ValidationError('Password xato')
        return password

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError('Password xato')

        return super().clean()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class OrderCreateForm(ModelForm):
    product = ModelChoiceField(queryset=Product.objects.all())
    stream = ModelChoiceField(queryset=Stream.objects.all(), required=False)
    phone_number = CharField()

    class Meta:
        model = Order
        fields = ('product', 'phone_number', 'full_name', 'stream', 'user')

    def clean_phone_number(self):
        phone_number = self.data.get('phone_number')
        return re.sub(r'[^\d]', '', phone_number)[-9:]


class StreamForm(ModelForm):
    product = ModelChoiceField(queryset=Product.objects.all())
    owner = ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Stream
        fields = 'name', 'discount', 'product', 'owner'


class FavoriteForm(ModelForm):
    class Meta:
        model = Favorite
        fields = "__all__"


class AuthAdminsLogin(AuthenticationForm):
    password = CharField(
        label=_("Password"),
        strip=False,
        widget=PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def clean_username(self):
        username = self.cleaned_data.get('username')


class OperatorUpdateForm(ModelForm):
    class Meta:
        model = Order
        fields = 'quantity', 'region', 'district', 'send_order_date', 'status',


class TransactionCreateForm(ModelForm):
    user = ModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Transaction
        fields = 'user', 'card_number', 'amount',

    def clean_card_number(self):
        card_number = self.data.get('card_number').replace(' ', '')
        if len(card_number) != 16:
            raise ValidationError("Karta raqamlari noto'gri bo'lishi mumkin tekshirib qaytadan uruning !!!")
        return card_number

    def save(self, commit=True):
        instance = super().save(commit=False)
        user = instance.user or self.user
        amount = self.cleaned_data.get('amount')
        if user.balance >= amount:
            user.balance -= amount
            user.save()
        else:
            raise ValidationError("Balansingizda yetarli mablag' mavjud emas .")
        if commit:
            instance.save()
        return instance


class OperatorOrderCreateForm(ModelForm):
    class Meta:
        model = Order
        fields = "full_name", "region", 'district', "quantity", "phone_number", "product",

    def clean_phone_number(self):
        phone_number = self.data.get('phone_number')
        return re.sub(r'[^\d]', '', phone_number)[-9:]
