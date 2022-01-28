package com.tutushubham.pythonscripttestapp

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.tutushubham.pythonscripttestapp.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)

        binding.testView.text = getString(R.string.used5)
        binding.centerButton.text = getString(R.string.used1)

        //val textview = findViewById<TextView>(R.id.test_view)
        //textview.setText(R.string.used1)
        setContentView(binding.root)
    }

}