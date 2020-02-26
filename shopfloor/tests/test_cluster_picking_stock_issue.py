from .test_cluster_picking_base import ClusterPickingCommonCase


class ClusterPickingStockIssue(ClusterPickingCommonCase):
    """Tests covering the /stock_issue endpoint
    """

    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(*args, **kwargs)
        # quants already existing are from demo data
        cls.env["stock.quant"].search(
            [("location_id", "=", cls.stock_location.id)]
        ).unlink()
        cls.batch = cls._create_picking_batch(
            [
                [
                    cls.BatchProduct(product=cls.product_a, quantity=10),
                    cls.BatchProduct(product=cls.product_b, quantity=15),
                ],
                [
                    cls.BatchProduct(product=cls.product_a, quantity=20),
                    cls.BatchProduct(product=cls.product_b, quantity=15),
                ],
                [
                    cls.BatchProduct(product=cls.product_a, quantity=30),
                    cls.BatchProduct(product=cls.product_b, quantity=15),
                ],
            ]
        )

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

    def _test_stock_issue(self, move_line, expected_initial_qty):
        product = move_line.product_id
        location = move_line.location_id
        qty = move_line.product_qty
        # no inventory yet
        self.assertFalse(self._find_inv_line(product, location))
        initial_qty = self.service._stock_issue_reserved_qty(product, location)
        self.assertEqual(initial_qty, expected_initial_qty)
        # file a stock issue
        self._stock_issue(move_line)
        # move line deleted
        self.assertFalse(move_line.exists())
        inv_line = self._find_inv_line(product, location)
        # qty must exclude current line qty
        self.assertEqual(inv_line.product_qty, initial_qty - qty)

    def test_stock_issue(self):
        self._simulate_batch_selected(self.batch, in_package=True)
        # work on product A line 1
        lineA = self.batch.picking_ids[0].move_line_ids.filtered(
            lambda x: x.product_id == self.product_a
        )
        self._test_stock_issue(lineA, 60)
        # work on product B
        lineB = self.batch.picking_ids[0].move_line_ids.filtered(
            lambda x: x.product_id == self.product_b
        )
        self._test_stock_issue(lineB, 45)
