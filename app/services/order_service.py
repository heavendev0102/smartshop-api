from decimal import Decimal

from app.repositories.cart_repo import CartRepository
from app.repositories.address_repo import AddressRepository
from app.repositories.delivery_option_repo import DeliveryOptionRepository
from app.repositories.order_repo import OrderRepository
from app.repositories.order_item_repo import OrderItemRepository

from app.schemas.order import (
    OrderPreviewRequest,
    OrderPreviewResponse,
    OrderCreateRequest,
    OrderCreateResponse,
    OrderDetailsResponse,
    OrderHistoryResponse,
    OrderHistoryProductResponse,
)

cart_repo = CartRepository()
address_repo = AddressRepository()
delivery_repo = DeliveryOptionRepository()
order_repo = OrderRepository()
order_item_repo = OrderItemRepository()


class OrderService:

    async def preview_order(
        self,
        db,
        user_id: int,
        body: OrderPreviewRequest,
    ) -> OrderPreviewResponse:

        address = await address_repo.get_by_id_for_user(
            db,
            body.address_id,
            user_id,
        )

        if not address:
            raise ValueError("Address not found")

        delivery_option = await delivery_repo.get_by_id(
            db,
            body.delivery_option_id,
        )

        if not delivery_option:
            raise ValueError("Delivery option not found")

        cart_items = await cart_repo.list_by_user(
            db,
            user_id,
        )

        if not cart_items:
            raise ValueError("Cart is empty")

        subtotal = Decimal("0.00")

        for item in cart_items:
            subtotal += (
                item.product.current_price
                * item.quantity
            )

        estimated_tax = Decimal("50.00")

        shipping_charge = Decimal(
            str(delivery_option.charge)
        )

        total = (
            subtotal
            + estimated_tax
            + shipping_charge
        )

        return OrderPreviewResponse(
            address=address.address,
            shipment_method=delivery_option.name,
            subtotal=subtotal,
            estimated_tax=estimated_tax,
            shipping_charge=shipping_charge,
            total=total,
        )

    async def place_order(
        self,
        db,
        user_id: int,
        body: OrderCreateRequest,
    ) -> OrderCreateResponse:

        VALID_PAYMENT_METHODS = {
            "credit_card",
            "paypal",
            "paypal_credit",
        }

        if body.payment_method not in VALID_PAYMENT_METHODS:
            raise ValueError("Invalid payment method")

        address = await address_repo.get_by_id_for_user(
            db,
            body.address_id,
            user_id,
        )

        if not address:
            raise ValueError("Address not found")

        delivery_option = await delivery_repo.get_by_id(
            db,
            body.delivery_option_id,
        )

        if not delivery_option:
            raise ValueError("Delivery option not found")

        cart_items = await cart_repo.list_by_user(
            db,
            user_id,
        )

        if not cart_items:
            raise ValueError("Cart is empty")

        subtotal = Decimal("0.00")

        for item in cart_items:
            subtotal += (
                item.product.current_price
                * item.quantity
            )

        estimated_tax = Decimal("50.00")

        shipping_charge = Decimal(
            str(delivery_option.charge)
        )

        total = (
            subtotal
            + estimated_tax
            + shipping_charge
        )

        order = await order_repo.create_order(
            db,
            {
                "user_id": user_id,
                "address_id": body.address_id,
                "delivery_option_id": body.delivery_option_id,
                "delivery_date": body.delivery_date,
                "payment_method": body.payment_method,
                "subtotal": subtotal,
                "estimated_tax": estimated_tax,
                "shipping_charge": shipping_charge,
                "total": total,
            },
        )

        for item in cart_items:

            line_total = (
                item.product.current_price
                * item.quantity
            )

            await order_repo.create_order_item(
                db,
                order.id,
                item.product_id,
                item.quantity,
                item.product.current_price,
                line_total,
            )

        await cart_repo.clear_for_user(
            db,
            user_id,
        )

        await order_repo.commit(db)

        return OrderCreateResponse(
            order_id=order.id,
            order_status=order.order_status,
            subtotal=subtotal,
            estimated_tax=estimated_tax,
            shipping_charge=shipping_charge,
            total=total,
        )

    async def get_order_details(
        self,
        db,
        user_id: int,
        order_id: int,
    ):

        order = await order_repo.get_by_id_for_user(
            db,
            order_id,
            user_id,
        )

        if not order:
            raise ValueError("Order not found")

        return OrderDetailsResponse(
            order_id=order.id,
            payment_method=order.payment_method,
            amount_paid=order.total,
            estimated_delivery=order.delivery_date,
            order_status=order.order_status,
        )

    async def get_order_history(
        self,
        db,
        user_id: int,
    ):

        orders = await order_repo.list_by_user(
            db,
            user_id,
        )

        response = []

        for order in orders:

            items = await order_item_repo.list_by_order(
                db,
                order.id,
            )

            products = []

            for item in items:
                products.append(
                    OrderHistoryProductResponse(
                        product_id=item.product_id,
                        product_name=item.product.name,
                        quantity=item.quantity,
                        unit_price=item.unit_price,
                        line_total=item.line_total,
                    )
                )

            response.append(
                OrderHistoryResponse(
                    order_id=order.id,
                    order_status=order.order_status,
                    payment_method=order.payment_method,
                    total=order.total,
                    delivery_date=order.delivery_date,
                    created_date=order.created_date,
                    products=products,
                )
            )

        return response