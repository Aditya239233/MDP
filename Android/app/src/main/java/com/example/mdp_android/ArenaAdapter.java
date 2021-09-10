package com.example.mdp_android;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import java.util.ArrayList;

public class ArenaAdapter extends ArrayAdapter<Arena> {
    public ArenaAdapter(@NonNull Context context, ArrayList<Arena> courseModelArrayList) {
        super(context, 0, courseModelArrayList);
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        View listitemView = convertView;
        if (listitemView == null) {
            // Layout Inflater inflates each item to be displayed in GridView.
            listitemView = LayoutInflater.from(getContext()).inflate(R.layout.card_item, parent, false);
        }
        Arena arena = getItem(position);
        ImageView block = listitemView.findViewById(R.id.idVBlock);
        block.setImageResource(arena.getImgid());
        return listitemView;
    }


}