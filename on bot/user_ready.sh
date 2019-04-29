#!/bin/bash
#	@file
#	@section COPYRIGHT
#	Copyright (C) 2017 Consequential Robotics (CqR)
#	
#	@section AUTHOR
#	Consequential Robotics http://consequentialrobotics.com
#	
#	@section LICENSE
#	For a full copy of the license agreement, see LICENSE.MDK in
#	the MDK root directory.
#	
#	Subject to the terms of this Agreement, Consequential Robotics
#	grants to you a limited, non-exclusive, non-transferable license,
#	without right to sub-license, to use MIRO Developer Kit in
#	accordance with this Agreement and any other written agreement
#	with Consequential Robotics. Consequential Robotics does not
#	transfer the title of MIRO Developer Kit to you; the license
#	granted to you is not a sale. This agreement is a binding legal
#	agreement between Consequential Robotics and the purchasers or
#	users of MIRO Developer Kit.
#	
#	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#	EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
#	OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#	NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#	HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#	WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#	FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#	OTHER DEALINGS IN THE SOFTWARE.
#	
#	@section DESCRIPTION
#	
#	This script is run once the wifi network has gone up and the
#	network connection is established. It's a great place to start
#	the run-time software; the user should configure this script.
#

# your actions here...

roscore
################################################################
##	UPDATED BY bridge_control.sh - DO NOT EDIT THIS SECTION!

# The line below is modified by bridge_control.sh when the user
# asks to change the bridge autostart status in MIROapp. If the
# line is to be changed manually, make sure only to add/remove
# the comment mark so that this continues to work correctly.
start_bridge.sh

##	UPDATED BY bridge_control.sh - DO NOT EDIT THIS SECTION!
################################################################





