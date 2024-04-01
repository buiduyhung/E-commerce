<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use App\Models\Product;

class ProductSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        Product::create([
            'title' => 'Product one',
            'price' => '19.03',
            'quantity' => '3',
            'category_id' => 1,
            'brand_id' => 1,
            'description' => 'product one',
        ]);
    }
}
