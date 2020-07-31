from .common import CommonCase


class ZonePickingCommonCase(CommonCase):
    @classmethod
    def setUpClassVars(cls, *args, **kwargs):
        super().setUpClassVars(*args, **kwargs)
        cls.menu = cls.env.ref("shopfloor.shopfloor_menu_zone_picking")
        cls.profile = cls.env.ref("shopfloor.shopfloor_profile_shelf_1_demo")
        cls.wh = cls.profile.warehouse_id
        cls.picking_type = cls.menu.picking_type_ids

    @classmethod
    def setUpClassBaseData(cls, *args, **kwargs):
        super().setUpClassBaseData(*args, **kwargs)
        cls.packing_location.sudo().active = True
        # We want to limit the tests to a dedicated location in Stock/ to not
        # be bothered with pickings brought by demo data
        cls.zone_location = (
            cls.env["stock.location"]
            .sudo()
            .create(
                {
                    "name": "Zone location",
                    "location_id": cls.stock_location.id,
                    "barcode": "ZONE_LOCATION",
                }
            )
        )
        cls.zone_sublocation1 = (
            cls.env["stock.location"]
            .sudo()
            .create(
                {
                    "name": "Zone sub-location 1",
                    "location_id": cls.zone_location.id,
                    "barcode": "ZONE_SUBLOCATION_1",
                }
            )
        )
        cls.zone_sublocation2 = (
            cls.env["stock.location"]
            .sudo()
            .create(
                {
                    "name": "Zone sub-location 2",
                    "location_id": cls.zone_location.id,
                    "barcode": "ZONE_SUBLOCATION_2",
                }
            )
        )
        cls.zone_sublocation3 = (
            cls.env["stock.location"]
            .sudo()
            .create(
                {
                    "name": "Zone sub-location 3",
                    "location_id": cls.zone_location.id,
                    "barcode": "ZONE_SUBLOCATION_3",
                }
            )
        )
        cls.zone_sublocation4 = (
            cls.env["stock.location"]
            .sudo()
            .create(
                {
                    "name": "Zone sub-location 4",
                    "location_id": cls.zone_location.id,
                    "barcode": "ZONE_SUBLOCATION_4",
                }
            )
        )
        cls.product_e = (
            cls.env["product.product"]
            .sudo()
            .create(
                {
                    "name": "Product E",
                    "type": "product",
                    "default_code": "E",
                    "barcode": "E",
                    "weight": 3,
                }
            )
        )
        cls.product_f = (
            cls.env["product.product"]
            .sudo()
            .create(
                {
                    "name": "Product F",
                    "type": "product",
                    "default_code": "F",
                    "barcode": "F",
                    "weight": 3,
                }
            )
        )
        products = (
            cls.product_a
            + cls.product_b
            + cls.product_c
            + cls.product_d
            + cls.product_e
            + cls.product_f
        )
        for product in products:
            cls.env["stock.putaway.rule"].sudo().create(
                {
                    "product_id": product.id,
                    "location_in_id": cls.stock_location.id,
                    "location_out_id": cls.shelf1.id,
                }
            )

        cls.picking1 = picking1 = cls._create_picking(lines=[(cls.product_a, 10)])
        cls.picking2 = picking2 = cls._create_picking(
            lines=[(cls.product_b, 10), (cls.product_c, 10)]
        )
        cls.picking3 = picking3 = cls._create_picking(lines=[(cls.product_d, 10)])
        cls.picking4 = picking4 = cls._create_picking(lines=[(cls.product_e, 10)])
        cls.picking5 = picking5 = cls._create_picking(
            lines=[(cls.product_b, 10), (cls.product_f, 10)]
        )
        cls.pickings = picking1 | picking2 | picking3 | picking4 | picking5
        cls._fill_stock_for_moves(
            picking1.move_lines, in_package=True, location=cls.zone_sublocation1
        )
        cls._fill_stock_for_moves(
            picking2.move_lines, in_lot=True, location=cls.zone_sublocation2
        )
        cls._fill_stock_for_moves(picking3.move_lines, location=cls.zone_sublocation3)
        cls._fill_stock_for_moves(
            picking5.move_lines, in_package=True, location=cls.zone_sublocation4
        )
        # Put product_e quantities in two different source locations to get
        # two stock move lines (6 and 4 to satisfy 10 qties)
        cls._update_qty_in_location(cls.zone_sublocation3, cls.product_e, 6)
        cls._update_qty_in_location(cls.zone_sublocation4, cls.product_e, 4)
        # cls._fill_stock_for_moves(picking4.move_lines, location=cls.zone_sublocation3)
        cls.pickings.action_assign()
        # Some records not related at all to the processed move lines
        cls.free_package = cls.env["stock.quant.package"].create(
            {"name": "FREE_PACKAGE"}
        )
        cls.free_lot = cls.env["stock.production.lot"].create(
            {
                "name": "FREE_LOT",
                "product_id": cls.product_a.id,
                "company_id": cls.env.company.id,
            }
        )
        cls.free_product = (
            cls.env["product.product"]
            .sudo()
            .create({"name": "FREE_PRODUCT", "barcode": "FREE_PRODUCT"})
        )

    def setUp(self):
        super().setUp()
        with self.work_on_services(menu=self.menu, profile=self.profile) as work:
            self.service = work.component(usage="zone_picking")

    def assert_response_start(self, response, message=None):
        self.assert_response(response, next_state="start", message=message)

    def _assert_response_select_picking_type(
        self, state, response, zone_location, picking_types, message=None
    ):
        self.assert_response(
            response,
            next_state=state,
            data={
                "zone_location": self.data.location(zone_location),
                "picking_types": self.data.picking_types(picking_types),
            },
            message=message,
        )

    def assert_response_select_picking_type(
        self, response, zone_location, picking_types, message=None
    ):
        self._assert_response_select_picking_type(
            "select_picking_type",
            response,
            zone_location,
            picking_types,
            message=message,
        )

    def _assert_response_select_line(
        self,
        state,
        response,
        zone_location,
        picking_type,
        move_lines,
        message=None,
        popup=None,
    ):
        self.assert_response(
            response,
            next_state=state,
            data={
                "zone_location": self.data.location(zone_location),
                "picking_type": self.data.picking_type(picking_type),
                "move_lines": self.data.move_lines(move_lines),
            },
            message=message,
            popup=popup,
        )

    def assert_response_select_line(
        self,
        response,
        zone_location,
        picking_type,
        move_lines,
        message=None,
        popup=None,
    ):
        self._assert_response_select_line(
            "select_line",
            response,
            zone_location,
            picking_type,
            move_lines,
            message=message,
            popup=popup,
        )

    def _assert_response_set_line_destination(
        self,
        state,
        response,
        zone_location,
        picking_type,
        move_line,
        message=None,
        confirmation_required=False,
    ):
        self.assert_response(
            response,
            next_state=state,
            data={
                "zone_location": self.data.location(zone_location),
                "picking_type": self.data.picking_type(picking_type),
                "move_line": self.data.move_line(move_line),
                "confirmation_required": confirmation_required,
            },
            message=message,
        )

    def assert_response_set_line_destination(
        self,
        response,
        zone_location,
        picking_type,
        move_line,
        message=None,
        confirmation_required=False,
    ):
        self._assert_response_set_line_destination(
            "set_line_destination",
            response,
            zone_location,
            picking_type,
            move_line,
            message=message,
            confirmation_required=confirmation_required,
        )

    def _assert_response_zero_check(
        self, state, response, zone_location, picking_type, location, message=None,
    ):
        self.assert_response(
            response,
            next_state=state,
            data={
                "zone_location": self.data.location(zone_location),
                "picking_type": self.data.picking_type(picking_type),
                "location": self.data.location(location),
            },
            message=message,
        )

    def assert_response_zero_check(
        self, response, zone_location, picking_type, location, message=None,
    ):
        self._assert_response_zero_check(
            "zero_check",
            response,
            zone_location,
            picking_type,
            location,
            message=message,
        )

    def _assert_response_change_pack_lot(
        self, state, response, zone_location, picking_type, move_line, message=None,
    ):
        self.assert_response(
            response,
            next_state=state,
            data={
                "zone_location": self.data.location(zone_location),
                "picking_type": self.data.picking_type(picking_type),
                "move_line": self.data.move_line(move_line),
            },
            message=message,
        )

    def assert_response_change_pack_lot(
        self, response, zone_location, picking_type, move_line, message=None,
    ):
        self._assert_response_change_pack_lot(
            "change_pack_lot",
            response,
            zone_location,
            picking_type,
            move_line,
            message=message,
        )

    def _assert_response_unload_set_destination(
        self,
        state,
        response,
        zone_location,
        picking_type,
        move_line,
        message=None,
        confirmation_required=False,
    ):
        self.assert_response(
            response,
            next_state=state,
            data={
                "zone_location": self.data.location(zone_location),
                "picking_type": self.data.picking_type(picking_type),
                "move_line": self.data.move_line(move_line),
                "confirmation_required": confirmation_required,
            },
            message=message,
        )

    def assert_response_unload_set_destination(
        self,
        response,
        zone_location,
        picking_type,
        move_line,
        message=None,
        confirmation_required=False,
    ):
        self._assert_response_unload_set_destination(
            "unload_set_destination",
            response,
            zone_location,
            picking_type,
            move_line,
            message=message,
            confirmation_required=confirmation_required,
        )

    def _assert_response_unload_all(
        self,
        state,
        response,
        zone_location,
        picking_type,
        move_lines,
        message=None,
        confirmation_required=False,
    ):
        self.assert_response(
            response,
            next_state=state,
            data={
                "zone_location": self.data.location(zone_location),
                "picking_type": self.data.picking_type(picking_type),
                "move_lines": self.data.move_lines(move_lines),
                "confirmation_required": confirmation_required,
            },
            message=message,
        )

    def assert_response_unload_all(
        self,
        response,
        zone_location,
        picking_type,
        move_lines,
        message=None,
        confirmation_required=False,
    ):
        self._assert_response_unload_all(
            "unload_all",
            response,
            zone_location,
            picking_type,
            move_lines,
            message=message,
            confirmation_required=confirmation_required,
        )

    def _assert_response_unload_single(
        self, state, response, zone_location, picking_type, move_line, message=None,
    ):
        self.assert_response(
            response,
            next_state=state,
            data={
                "zone_location": self.data.location(zone_location),
                "picking_type": self.data.picking_type(picking_type),
                "move_line": self.data.move_line(move_line),
            },
            message=message,
        )

    def assert_response_unload_single(
        self, response, zone_location, picking_type, move_line, message=None,
    ):
        self._assert_response_unload_single(
            "unload_single",
            response,
            zone_location,
            picking_type,
            move_line,
            message=message,
        )