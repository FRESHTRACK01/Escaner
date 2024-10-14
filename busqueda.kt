package com.example.fresh_track


import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.ImageButton
import android.widget.ImageView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import com.google.zxing.integration.android.IntentIntegrator
import com.google.zxing.integration.android.IntentResult

class busqueda : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_busqueda)

        val men = findViewById<ImageButton>(R.id.icon_two)
        men.setOnClickListener {
            val intent = Intent(this, inventario::class.java)
            startActivity(intent)
        }

        val btn1 = findViewById<Button>(R.id.btn_guar)
        btn1.setOnClickListener {

            Toast.makeText(this, "Cambios guardados", Toast.LENGTH_SHORT).show()

            btn1.postDelayed({
                val intent = Intent(this, inventario::class.java)
                startActivity(intent)
            }, 1000)
        }


        val scanButton = findViewById<ImageView>(R.id.icon_escan)
        scanButton.setOnClickListener {
            initiateScan()
        }
    }


    private fun initiateScan() {
        val integrator = IntentIntegrator(this)
        integrator.setOrientationLocked(false)
        integrator.initiateScan()
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        val result: IntentResult = IntentIntegrator.parseActivityResult(requestCode, resultCode, data)
        if (result != null) {
            if (result.contents == null) {
                Toast.makeText(this, "Escaneo cancelado", Toast.LENGTH_LONG).show()
            } else {

                Toast.makeText(this, "Código escaneado: ${result.contents}", Toast.LENGTH_LONG).show()
            }
        } else {
            super.onActivityResult(requestCode, resultCode, data)
        }
    }
}