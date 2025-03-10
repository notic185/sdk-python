from typing import Optional, Any, List


class Result:
    def __init__(self, code: int = None, message: str = None, data: Any = None):
        self.code = code
        self.message = message
        self.data = data


class Model:
    def __init__(self, id: Optional[str] = None, uuid: Optional[str] = None, version: int = None,
                 deleted_at: Optional[str] = None, created_at: Optional[str] = None,
                 updated_at: Optional[str] = None):
        self.id = id
        self.uuid = uuid
        self.version = version
        self.deleted_at = deleted_at
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "version": self.version,
            "deleted_at": self.deleted_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class NamedModel:
    def __init__(self, name: Optional[str] = None, description: Optional[str] = None):
        self.name = name
        self.description = description

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
        }


class OwnedModel:
    def __init__(self, user: Optional['User'] = None, owner: Optional['User'] = None):
        self.user = user
        self.owner = owner

    def to_dict(self):
        return {
            "user": self.user,
            "owner": self.owner,
        }


class OrderCallback:
    def __init__(self, endpoint: Optional[str] = None, model: Optional[Model] = None):
        self.endpoint = endpoint
        self.model = model if model else Model()

    def to_dict(self):
        return {
            "endpoint": self.endpoint,
            "model": self.model.to_dict()
        }


class UserCredential:
    def __init__(self, external_id: Optional[str] = None, secret: Optional[str] = None,
                 model: Optional[Model] = None, named_model: Optional[NamedModel] = None,
                 owned_model: Optional[OwnedModel] = None):
        self.external_id = external_id
        self.secret = secret
        self.model = model if model else Model()
        self.named_model = named_model if named_model else NamedModel()
        self.owned_model = owned_model if owned_model else OwnedModel()

    def to_dict(self):
        return {
            "external_id": self.external_id,
            "secret": self.secret,
            "model": self.model.to_dict(),
            "named_model": self.named_model.to_dict() if self.named_model else None,
            "owned_model": self.owned_model.to_dict() if self.owned_model else None
        }


class MerchantOrder:
    def __init__(self, merchant: Optional['User'] = None, order: Optional['Order'] = None,
                 external_ip_for_creator: Optional[str] = None, external_ip_for_payer: Optional[str] = None,
                 model: Optional[Model] = None, named_model: Optional[NamedModel] = None,
                 owned_model: Optional[OwnedModel] = None):
        self.merchant = merchant if merchant else User()
        self.order = order if order else Order()
        self.external_ip_for_creator = external_ip_for_creator
        self.external_ip_for_payer = external_ip_for_payer
        self.model = model if model else Model()
        self.named_model = named_model if named_model else NamedModel()
        self.owned_model = owned_model if owned_model else OwnedModel()

    def to_dict(self):
        return {
            "merchant": self.merchant.to_dict(),
            "order": self.order.to_dict(),
            "external_ip_for_creator": self.external_ip_for_creator,
            "external_ip_for_payer": self.external_ip_for_payer,
            "model": self.model.to_dict(),
            "named_model": self.named_model.to_dict() if self.named_model else None,
            "owned_model": self.owned_model.to_dict() if self.owned_model else None
        }


class Order:
    def __init__(self, order_transaction_id: Optional[str] = None, status: Optional[str] = None,
                 amount: Optional[str] = None, integral_amount: Optional[str] = None,
                 external_id: Optional[str] = None, code: Optional[str] = None,
                 order_callback: Optional[OrderCallback] = None,
                 model: Optional[Model] = None, named_model: Optional[NamedModel] = None,
                 owned_model: Optional[OwnedModel] = None, **kwargs):
        self.order_transaction_id = order_transaction_id
        self.status = status
        self.amount = amount
        self.integral_amount = integral_amount
        self.external_id = external_id
        self.code = code
        self.order_callback = order_callback if order_callback else OrderCallback()
        self.model = model if model else Model()
        self.named_model = named_model if named_model else NamedModel()
        self.owned_model = owned_model if owned_model else OwnedModel()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        return {
            "order_transaction_id": self.order_transaction_id,
            "status": self.status,
            "amount": self.amount,
            "integral_amount": self.integral_amount,
            "external_id": self.external_id,
            "code": self.code,
            "order_callback": self.order_callback.to_dict(),
            "model": self.model.to_dict(),
            "named_model": self.named_model.to_dict(),
            "owned_model": self.owned_model.to_dict()
        }


class User:
    def __init__(self, user_type: Optional[str] = None, log_status: Optional[str] = None, integral: Optional[str] = None,
                 last_seen_at: Optional[str] = None, model: Optional[Model] = None,
                 named_model: Optional[NamedModel] = None):
        self.user_type = user_type
        self.log_status = log_status
        self.integral = integral
        self.last_seen_at = last_seen_at
        self.model = model if model else Model()
        self.named_model = named_model if named_model else NamedModel()

    def to_dict(self):
        return {
            "user_type": self.user_type,
            "log_status": self.log_status,
            "integral": self.integral,
            "last_seen_at": self.last_seen_at,
            "model": self.model.to_dict(),
            "named_model": self.named_model.to_dict(),
        }


class UserOrder:
    def __init__(self, currency: Optional[str] = None, order: Optional[Order] = None,
                 model: Optional[Model] = None, named_model: Optional[NamedModel] = None,
                 owned_model: Optional[OwnedModel] = None):
        self.currency = currency
        self.order = order
        self.model = model if model else Model()
        self.named_model = named_model if named_model else NamedModel()
        self.owned_model = owned_model if owned_model else OwnedModel()

    def to_dict(self):
        return {
            "currency": self.currency,
            "order": self.order,
            "model": self.model.to_dict(),
            "named_model": self.named_model.to_dict(),
            "owned_model": self.owned_model.to_dict()
        }


class UserWallet:
    def __init__(self, status: Optional[str] = None, user_wallet_type: Optional[str] = None, acceptable_range: List[Any] = None,
                 last_used_at: Optional[str] = None, user_wallet_attributes: List['UserWalletAttribute'] = None,
                 model: Optional[Model] = None, named_model: Optional[NamedModel] = None,
                 owned_model: Optional[OwnedModel] = None):
        self.status = status
        self.user_wallet_type = user_wallet_type
        self.acceptable_range = acceptable_range if acceptable_range else []
        self.last_used_at = last_used_at
        self.user_wallet_attributes = user_wallet_attributes if user_wallet_attributes else []
        self.model = model if model else Model()
        self.named_model = named_model if named_model else NamedModel()
        self.owned_model = owned_model if owned_model else OwnedModel()

    def to_dict(self):
        return {
            "status": self.status,
            "user_wallet_type": self.user_wallet_type,
            "acceptable_range": self.acceptable_range,
            "last_used_at": self.last_used_at,
            "user_wallet_attributes": self.user_wallet_attributes,
            "model": self.model.to_dict(),
            "named_model": self.named_model.to_dict(),
            "owned_model": self.owned_model.to_dict()
        }


class UserWalletAttribute:
    def __init__(self, key: Optional[str] = None, value: Optional[str] = None,
                 model: Optional[Model] = None, owned_model: Optional[OwnedModel] = None):
        self.key = key
        self.value = value
        self.model = model if model else Model()
        self.owned_model = owned_model if owned_model else OwnedModel()

    def to_dict(self):
        return {
            "key": self.key,
            "value": self.value,
            "model": self.model.to_dict(),
            "owned_model": self.owned_model.to_dict()
        }
