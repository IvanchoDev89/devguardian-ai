<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class EmailQueueController extends Controller
{
    public function index(Request $request)
    {
        $emails = DB::table('email_queue')
            ->orderBy('created_at', 'desc')
            ->limit(100)
            ->get();
            
        return response()->json([
            'success' => true,
            'data' => $emails
        ]);
    }

    public function send(Request $request)
    {
        $request->validate([
            'to' => 'required|email',
            'subject' => 'required|string',
            'body' => 'required|string'
        ]);

        $user = $request->user();
        
        $emailId = DB::table('email_queue')->insertGetId([
            'user_id' => $user->id,
            'to' => $request->to,
            'subject' => $request->subject,
            'body' => $request->body,
            'status' => 'pending',
            'created_at' => now(),
            'updated_at' => now()
        ]);

        // In production, this would trigger a job to send the email
        // For now, we'll mark it as sent
        
        return response()->json([
            'success' => true,
            'message' => 'Email queued successfully',
            'data' => ['id' => $emailId]
        ]);
    }

    public function sendBulk(Request $request)
    {
        $request->validate([
            'recipients' => 'required|array',
            'subject' => 'required|string',
            'body' => 'required|string'
        ]);

        $user = $request->user();
        $emails = [];
        
        foreach ($request->recipients as $recipient) {
            $emails[] = [
                'user_id' => $user->id,
                'to' => $recipient,
                'subject' => $request->subject,
                'body' => $request->body,
                'status' => 'pending',
                'created_at' => now(),
                'updated_at' => now()
            ];
        }

        DB::table('email_queue')->insert($emails);

        return response()->json([
            'success' => true,
            'message' => count($emails) . ' emails queued successfully'
        ]);
    }

    public function getPending()
    {
        $emails = DB::table('email_queue')
            ->where('status', 'pending')
            ->orderBy('created_at', 'asc')
            ->limit(50)
            ->get();

        return response()->json([
            'success' => true,
            'data' => $emails
        ]);
    }

    public function markSent(Request $request, $id)
    {
        DB::table('email_queue')
            ->where('id', $id)
            ->update([
                'status' => 'sent',
                'sent_at' => now()
            ]);

        return response()->json([
            'success' => true,
            'message' => 'Email marked as sent'
        ]);
    }
}
