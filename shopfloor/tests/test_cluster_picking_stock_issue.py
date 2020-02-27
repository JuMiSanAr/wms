from .test_cluster_picking_base import ClusterPickingCommonCase


class ClusterPickingStockIssue(ClusterPickingCommonCase):
    """Tests covering the /stock_issue endpoint
    """

    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(*args, **kwargs)
        # quants already existing are from demo data
        loc_ids = (cls.stock_location.id, cls.shelf1.id, cls.shelf2.id)
        cls.env["stock.quant"].search([("location_id", "in", loc_ids)]).unlink()
        cls.shelf_Z = cls.shelf2.copy({"name": "Shelf Z", "barcode": "SHELF-Z"})
        cls._update_qty_in_location(cls.shelf1, cls.product_a, 3)
        cls._update_qty_in_location(cls.shelf2, cls.product_a, 50)
        cls._update_qty_in_location(cls.shelf_Z, cls.product_a, 100)
        cls.batch = cls._create_picking_batch(
            [
                [cls.BatchProduct(product=cls.product_a, quantity=10)],
                [cls.BatchProduct(product=cls.product_a, quantity=20)],
            ]
        )
        cls.batch1 = cls._create_picking_batch(
            [[cls.BatchProduct(product=cls.product_a, quantity=30)]]
        )
        # TODO
        # put the same product in the same picking in 2 diff locations
        # location X: qty 3, location Y: 100
        # create location Z, qty 200 not assigned (just set qty on hand)

        # simulate 1st prod A in location X move line is done
        # a move line w/ qty done == qty3

        # select both batches (we need the pickings to be confirmed/assigned)
        #
        # TEST
        # use the line in location Y and trigger stock issue
        # result:
        # 1. inv line w/ qty 27
        # 1a. in location Y as we created the inventory we should not have any move line for prod A
        # and make sure that loc Z has 197 available

        # 2. control inventory created
        # 3. reserve again => check that the line w/ qty 3 is back
        # WATCH OUT: likely the qty done will be ZERO instead of 3
        # if this happens consider doing the same thing as here
        # https://github.com/camptocamp/alcyon_odoo/blob/master/odoo/local-src/stock_operation_recompute/models/stock_move.py#L24
        # to restore the qty done
        #

    def _stock_issue(self, line, next_line=None):
        response = self.service.dispatch(
            "stock_issue", params={"move_line_id": line.id}
        )
        if next_line:
            self.assert_response(
                response, next_state="start_line", data=self._line_data(next_line)
            )
        return response

    def _find_inv_line(self, product, location):
        inv_line_model = self.env["stock.inventory.line"]
        domain = [("product_id", "=", product.id), ("location_id", "=", location.id)]
        return inv_line_model.search(domain, limit=1)

    def _test_stock_issue(self, move_line, expected_unreserved_qty):
        product = move_line.product_id
        location = move_line.location_id
        qty = move_line.product_qty
        # no inventory yet
        self.assertFalse(self._find_inv_line(product, location))
        self.assertFalse(self.service._control_inventory_exists(product, location))
        # file a stock issue
        self._stock_issue(move_line)
        # move line deleted
        self.assertFalse(move_line.exists())
        inv_line = self._find_inv_line(product, location)
        # qty ok
        self.assertEqual(inv_line.product_qty, expected_unreserved_qty)
        # control inventory created
        self.assertTrue(self.service._control_inventory_exists(product, location))

    def _check_qty(self, prod, loc, expected_qty):
        self.assertEqual(
            self.env["stock.quant"]._get_available_quantity(prod, loc), expected_qty
        )

    def test_stock_issue(self):
        self._simulate_batch_selected(self.batch, in_package=True)
        self._simulate_batch_selected(self.batch1, in_package=True)
        # verify expected quantities
        # all booked on shelf 1 and 2
        self._check_qty(self.product_a, self.shelf1, 0)
        self._check_qty(self.product_a, self.shelf2, 0)
        # something left on Z
        self._check_qty(self.product_a, self.shelf_Z, 93)
        # work on product A line 1
        lines_a = self.batch.picking_ids[0].move_line_ids.filtered(
            lambda x: x.product_id == self.product_a
        )
        # DEVs: to check all move lines here
        # self.batch.mapped('picking_ids.move_line_ids').read([
        # 'move_id', 'product_qty', 'qty_done',
        # 'location_id', 'location_dest_id', 'picking_id'
        # ])
        #
        batch1_lines = self.batch.mapped("picking_ids.move_line_ids")
        # As in location 1 we have only 3 products available
        # we'll have 2 lines to satisfy the picking w/ 20.0 prods:
        # 3 coming from shelf 1, 17 coming from shelf 2
        # Then 1 line to satisfy the 10.0, from shelf 2.
        # FIXME: this is random depending on where the products are taken
        # and it could be `[3.0, 7.0, 20.0]` instead
        # self.assertEqual(
        #     sorted(batch1_lines.mapped('product_qty')),
        #     [3.0, 10.0, 17.0]
        # )
        # let's pick the line w/ 3 and do it
        line3 = batch1_lines.filtered(lambda x: x.product_qty == 3.0)
        # it comes from shelf 1
        self.assertEqual(line3.location_id, self.shelf1)
        # make it happy
        line3.qty_done = line3.product_qty
        line3._action_done()
        # now let's declare a stock issue on the one w/ 17 products
        line17 = batch1_lines.filtered(lambda x: x.product_qty == 17.0)
        self.assertEqual(line17.location_id, self.shelf2)
        # TODO @simahawk: not sure about this number
        self._test_stock_issue(line17, 50)
        # make sure the qty done on line3 is still there
        # FIXME: this fails ATM because the line is deleted
        self.assertEqual(line3.qty_done, 3.0)

        # # work on product B
        # lineB = self.batch.picking_ids[0].move_line_ids.filtered(
        #     lambda x: x.product_id == self.product_b
        # )
        # self._test_stock_issue(lineB, 45)
