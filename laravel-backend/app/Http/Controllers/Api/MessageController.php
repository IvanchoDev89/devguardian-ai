<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class MessageController extends Controller
{
    public function index(Request $request)
    {
        $user = $request->user();
        
        $messages = DB::table('messages')
            ->where('receiver_id', $user->id)
            ->orWhere('sender_id', $user->id)
            ->orderBy('created_at', 'desc')
            ->limit(50)
            ->get();
            
        return response()->json([
            'success' => true,
            'data' => $messages
        ]);
    }

    public function send(Request $request)
    {
        $request->validate([
            'receiver_id' => 'required|exists:users,id',
            'subject' => 'nullable|string',
            'body' => 'required|string',
            'type' => 'nullable|in:message,alert,notification',
            'priority' => 'nullable|in:low,normal,high,urgent'
        ]);

        $user = $request->user();
        
        $messageId = DB::table('messages')->insertGetId([
            'sender_id' => $user->id,
            'receiver_id' => $request->receiver_id,
            'subject' => $request->subject,
            'body' => $request->body,
            'type' => $request->type ?? 'message',
            'priority' => $request->priority ?? 'normal',
            'created_at' => now(),
            'updated_at' => now()
        ]);

        return response()->json([
            'success' => true,
            'message' => 'Message sent successfully',
            'data' => ['id' => $messageId]
        ]);
    }

    public function markAsRead(Request $request, $id)
    {
        $user = $request->user();
        
        DB::table('messages')
            ->where('id', $id)
            ->where('receiver_id', $user->id)
            ->update([
                'is_read' => true,
                'read_at' => now()
            ]);

        return response()->json([
            'success' => true,
            'message' => 'Message marked as read'
        ]);
    }

    public function unreadCount(Request $request)
    {
        $user = $request->user();
        
        $count = DB::table('messages')
            ->where('receiver_id', $user->id)
            ->where('is_read', false)
            ->count();

        return response()->json([
            'success' => true,
            'data' => ['unread_count' => $count]
        ]);
    }
}
